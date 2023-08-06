import logging
import threading
from typing import Optional

import zmq

from openmodule.alert import AlertHandler
from openmodule.config import validate_config_module
from openmodule.health import HealthHandlerType, Healthz
from openmodule.logging import init_logging
from openmodule.messaging import get_pub_socket, get_sub_socket, receive_message_from_socket
from openmodule.models import ZMQMessage
from openmodule.sentry import init_sentry
from openmodule.threading import get_thread_wrapper


class OpenModuleCore(threading.Thread):
    def __init__(self, context, config):
        super().__init__(target=get_thread_wrapper(self._run))
        self.context = context
        self.config = config
        self.pub_lock = threading.Lock()
        self.pub_socket = get_pub_socket(self.context, self.config, linger=1000)
        self.sub_socket = get_sub_socket(self.context, self.config)
        self.sub_socket.subscribe(b"healthz")
        self.log = logging.getLogger(self.__class__.__name__)

        self.health = Healthz(self)
        self.alerts = AlertHandler(self)

    def _run(self):
        try:
            while True:
                topic, message = receive_message_from_socket(self.sub_socket)
                if message is None:
                    continue
                if topic == b"healthz":
                    self.health.process_message(message)
        except zmq.ContextTerminated:
            self.log.debug("context terminated, core shutting down")
        finally:
            self.pub_socket.close()
            self.sub_socket.close()

    def publish(self, message: ZMQMessage, topic: bytes):
        with self.pub_lock:
            message.publish_on_topic(self.pub_socket, topic)


_core_thread: Optional[OpenModuleCore] = None


def init_openmodule(config, sentry=True, logging=True,
                    health_handler: Optional[HealthHandlerType] = None,
                    context=None) -> OpenModuleCore:
    context = context or zmq.Context()
    validate_config_module(config)

    global _core_thread
    assert not _core_thread, "openmodule core already running"
    _core_thread = OpenModuleCore(context, config)
    _core_thread.start()

    if logging:
        init_logging(_core_thread)

    if sentry:
        init_sentry(_core_thread)

    if health_handler:
        _core_thread.health.health_handler = health_handler

    return _core_thread


def core():
    return _core_thread


def shutdown_openmodule():
    global _core_thread
    assert _core_thread, "core thread is not running, did you call init_openmodule(...)?"

    _core_thread.context.term()
    _core_thread.join()

    _core_thread = None
