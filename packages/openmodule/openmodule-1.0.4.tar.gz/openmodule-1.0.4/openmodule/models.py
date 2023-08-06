import orjson
import time
import zmq
from pydantic import Field, BaseModel


def _donotuse(v, *, default):
    assert False, "please use json_bytes"


class OpenModuleModel(BaseModel):
    class Config:
        validate_assignment = True

        json_loads = orjson.loads
        json_dumps = _donotuse

    def json_bytes(self):
        return orjson.dumps(self.dict(exclude_none=True))


class ZMQMessage(OpenModuleModel):
    timestamp: float = Field(default_factory=time.time)
    name: str
    type: str

    def publish_on_topic(self, pub_socket: zmq.Socket, topic: bytes):
        pub_socket.send_multipart((topic, self.json_bytes()))
