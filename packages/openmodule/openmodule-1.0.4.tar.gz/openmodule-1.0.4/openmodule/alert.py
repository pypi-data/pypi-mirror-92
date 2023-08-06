import logging
import threading
from enum import Enum
from typing import TYPE_CHECKING, List, Dict, Optional

from pydantic import validator

from openmodule.models import ZMQMessage

if TYPE_CHECKING:  # pragma: no cover
    from openmodule.core import OpenModuleCore


class AlertStatus(str, Enum):
    ok = "ok"
    error = "error"
    offline = "offline"


class AlertHandleType(str, Enum):
    state = "state"
    state_change = "state_change"
    count = "count"


class AlertMessage(ZMQMessage):
    type: str = "alert"
    status: AlertStatus
    alert_meta: Dict
    package: str
    alert_type: str
    source: Optional[str]
    handle_type: AlertHandleType
    value: Optional[float]

    @validator("value")
    def require_value_for_state_type(cls, v, values):
        if values["handle_type"] == AlertHandleType.state:
            assert v is not None, "value must not be None for alerts with handle_type='state'"
        return v


class AlertHandler(object):
    _alerts: List[Dict]

    def __init__(self, core: 'OpenModuleCore'):
        self._alerts = []
        self._alerts_lock = threading.RLock()
        self.core = core
        self.log = logging.getLogger(self.__class__.__name__)

    def _send_message(self, alert_id, status_dict):
        alert = self._alerts[alert_id]
        if alert["alert_dict"]["handle_type"] == AlertHandleType.state and status_dict.get("value") is None:
            raise ValueError("value must not be none for alerts with handle_type=state")

        status_dict["alert_meta"].update(dict(sender=self.core.config.NAME))
        old_status = alert["alert_dict"].get("status")
        alert["alert_dict"].update(status_dict)
        if alert["always_send_alert"] or alert["alert_dict"]["status"] != old_status:
            message = AlertMessage(
                name=self.core.config.NAME,
                type="alert",
                **alert["alert_dict"]
            )

            package = message.package if message.package != self.core.config.NAME else ""
            source = message.source
            tmp = f"{' from ' if package or source else ''}{package}{'/' if package and source else ''}{source}:"
            self.log.info(f"Send alert{tmp} {message.alert_type} - {message.status}")

            self.core.publish(message, b"alert")
            return True
        return False

    def get_or_add_alert_id(self, source: str, alert_type: str, handle_type: AlertHandleType,
                            package_name: Optional[str] = None, version: Optional[str] = None,
                            always_send_alert: Optional[bool] = None):
        """Define an alert with its name parameters

        Args:
            source (str): The source of the error (i.e. which pin, camera)
            alert_type (str): Name of the alert all lower_case with '_' (i.e. high_time_check)
            handle_type (str): How the error should be handled on the server (state, state_change, count)
            package_name (str) (default=config.NAME): You send the error for this package
            version (str) (default=config.VERSION): Current version of the package
            always_send_alert (bool) (default=False): Send every alert or only when there is a change in the status

        Returns:
            alert_id of the saved alert
        """

        assert "-" not in alert_type, "please do not use '-' in your alert type names"

        alert_dict = dict(source=source, alert_type=alert_type, handle_type=handle_type)
        alert_dict["package"] = package_name or self.core.config.NAME

        with self._alerts_lock:
            for alert in self._alerts:
                if alert_dict.items() <= alert["alert_dict"].items():
                    if always_send_alert is not None:
                        alert["always_send_alert"] = always_send_alert
                    if version is not None:
                        alert["alert_dict"]["version"] = version
                    return alert["id"]

            v = version if version is not None else self.core.config.VERSION
            asa = always_send_alert if always_send_alert is not None else False
            alert = {"alert_dict": alert_dict, "id": len(self._alerts), "always_send_alert": asa, "version": v}
            self._alerts.append(alert)
            return alert["id"]

    def send_with_alert_id(self, alert_id: int, status: AlertStatus, meta: Dict, value: Optional[float] = None):
        """ Send a status message on the given alert with the corresponding meta/kwarg arguments
            Returns True if alert was send else False"""
        assert status in [AlertStatus.error, AlertStatus.ok, AlertStatus.offline]

        status_dict = {
            "status": status,
            "alert_meta": (meta or {}),
        }
        if value is not None:
            status_dict["value"] = value

        return self._send_message(alert_id, status_dict)

    def send(self, source: str, alert_type: str, handle_type: AlertHandleType,
             package_name: Optional[str] = None, version: Optional[str] = None,
             always_send_alert: Optional[bool] = None, status: AlertStatus = AlertStatus.error,
             meta: Optional[Dict] = None, value: Optional[float] = None):

        """Sends an alert to the device serve

        Args:
            source (str): The source of the error (i.e. which pin, camera)
            alert_type (str): Name of the alert all lower_case with '_' (i.e. high_time_check, health_hw_compute_nuc)
            handle_type (str): How the error should be handled on the server (state, state_change, count)
            status (Status/bool): The status you want to send(Status.OK/True, Status.ERROR/False, Status.OFFLINE)
            package_name (str) optional: You can send errors for other packages
            version (str) (default=config.VERSION): Current version of the package
            always_send_alert (bool): Flag to declare if you want to send every alert or only every change in the status
            meta (dict): Meta information
            value (float): value of the error metric, only applicable if handle_type=state

        Returns:
            True if alert was send else False
        """
        assert "-" not in alert_type, "please do not use - in your alert type names"

        alert_id = self.get_or_add_alert_id(source, alert_type, handle_type, package_name, version, always_send_alert)
        return self.send_with_alert_id(alert_id, status, meta, value)
