import os
import sys
import traceback
from collections import namedtuple
from typing import Callable, Any, Dict, Optional, Type

import logging
import sentry_sdk
import threading
import time
import zmq
from pydantic import ValidationError, BaseModel
from uuid import UUID

from openmodule.messaging import get_sub_socket, get_pub_socket, receive_message_from_socket
from openmodule.models import ZMQMessage
from openmodule.rpc.common import channel_to_request_topic, channel_to_response_topic
from openmodule.threading import get_thread_wrapper

CallbackEntry = namedtuple("CallbackEntry", ["timestamp", "result"])
HandlerEntry = namedtuple("HandlerEntry", ["request_class", "response_class", "handler"])


class RPCRequest(ZMQMessage):
    rpc_id: UUID
    request: Optional[Dict]


class RPCResponse(ZMQMessage):
    rpc_id: Optional[UUID]
    response: Any


def gateway_filter(gate=None, direction=None):
    def _filter(request, message, handler):
        gateway = request.get("gateway")
        if not gateway:
            return False
        return (not gate or gate == gateway.get("gate")) and \
               (not direction or direction == gateway.get("direction"))

    return _filter


class RPCServer(object):
    def __init__(self, context, config):
        self.name = config.NAME
        self.sub = get_sub_socket(context, config)
        self.pub = get_pub_socket(context, config)
        self.handlers: Dict[tuple, HandlerEntry] = {}
        self.filters = []
        self.running = True
        self.log = logging.getLogger(self.__class__.__name__)
        self.thread = None

    def add_filter(self, filter: Callable[[], bool]):
        self.filters.append(filter)

    def shutdown(self, timeout=3):
        self.running = False
        if self.thread:
            self.thread.join(timeout=timeout)

    def register_handler(self, channel: str, type: str, request_class: Type[BaseModel], response_class: Type[BaseModel],
                         handler: Callable):
        """
        :param channel: rpc channel you want to subscribe to, patterns/wildcards are not supported
        :param type: the request type
        :param handler: request handler of the form (request:dict, meta:dict) -> any
                        if the handler returns a dict which contains the key "status",
                        then the value of "status" will be used as the rpc response status.
                        There are no other reserved keys except "status".
        """
        if (channel, type) in self.handlers:
            raise ValueError(f"handler for {channel}:{type} is already registered")

        self.log.debug("register handler {}:{} -> {}".format(channel, type, handler))
        self.sub.subscribe(channel_to_request_topic(channel.encode("ascii")))
        self.handlers[(channel, type)] = HandlerEntry(request_class, response_class, handler)

    def _channel_from_topic(self, topic: bytes) -> str:
        return topic.split(b"-", 2)[-1].decode("ascii")

    def should_process_message(self, request, message, handler):
        if self.filters:
            for filter in self.filters:
                if filter(request=request, message=message, handler=handler):
                    return True
            return False
        return True

    def find_handler(self, channel: str, type: str) -> HandlerEntry:
        return self.handlers.get((channel, type))

    def run_as_thread(self):
        assert not self.thread, "cannot run the same rpc server multiple times as thread"
        self.thread = threading.Thread(target=get_thread_wrapper(self.run))
        self.thread.start()
        return self.thread

    def process_rpc(self, channel, message: RPCRequest) -> Optional[Dict]:
        handler: HandlerEntry = self.find_handler(channel, message.type)
        if handler:
            try:
                request = handler.request_class(**message.request)
            except ValidationError as e:
                return {"status": "validation_error", "exception": e.json()}

            try:
                if not self.should_process_message(request, message, handler):
                    return None
            except Exception as e:
                self.log.exception("exception in message filter. request not processed and error returned")
                return {"status": "filter_error", "exception": str(e)}

            try:
                response = handler.handler(request, message)
                if isinstance(response, dict):
                    return handler.response_class(**response).dict()
                elif response is None:
                    return {}  # None is used for when we do not handle the function, so we convert to dict here
                elif isinstance(response, handler.response_class):
                    return response.dict()
                else:
                    raise Exception("rpc handler must return None, a dict or a instance of its response_class")
            except Exception as e:
                self.log.exception("exception in handler {}:{}".format(channel, type))
                return {"status": "handler_error", "exception": str(e)}
        else:
            self.log.warning("no handler found for {}:{}".format(channel, type))
            return None

    def run(self):
        poller = zmq.Poller()
        poller.register(self.sub, zmq.POLLIN)
        try:
            while self.running:
                socks = dict(poller.poll(timeout=1000))
                if socks.get(self.sub) != zmq.POLLIN:
                    continue
                topic, message = receive_message_from_socket(self.sub)
                if topic is None:
                    continue
                channel = self._channel_from_topic(topic)

                try:
                    message = RPCRequest(**message)
                    message_type = message.type
                    rpc_id = message.rpc_id
                except ValidationError as e:
                    message_type = "unknown"
                    rpc_id = None
                    response = {"status": "validation_error", "exception": e.json()}
                else:
                    response = self.process_rpc(channel, message)

                if response is not None:
                    self.log.debug("response: {}".format(response))
                    if "status" not in response:
                        response["status"] = "ok"

                    result = RPCResponse(
                        type=message_type,
                        rpc_id=rpc_id,
                        response=response,
                        name=self.name
                    )
                    result.publish_on_topic(
                        self.pub,
                        channel_to_response_topic(channel.encode("ascii")),
                    )
        except zmq.ContextTerminated:
            pass
        finally:
            self.sub.close()
            self.pub.close()
