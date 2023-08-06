from typing import Optional
from unittest import TestCase

import orjson

from openmodule.models import OpenModuleModel, ZMQMessage


class TestModel(OpenModuleModel):
    __test__ = False
    value: str


class ModelTestCase(TestCase):

    def test_json_is_forbidden(self):
        instance = TestModel(value="Hello World")
        with self.assertRaises(AssertionError):
            instance.json()

    def test_json_dumps_and_load(self):
        instance = TestModel(value="Hello World")
        instance2 = TestModel.parse_raw(instance.json_bytes())
        self.assertEqual(instance.value, instance2.value)

    def test_unset_default_are_serialized(self):
        class SomeZMQMessage(ZMQMessage):
            type: str = "my-type"

        msg = SomeZMQMessage(name="myname").json_bytes()
        data = orjson.loads(msg)

        self.assertIn("type", data)
        self.assertEqual("my-type", data.get("type"))

    def test_none_values_are_not_exported(self):
        class SomeZMQMessage(ZMQMessage):
            type: str = "test"
            value: Optional[float]

        data = orjson.loads(SomeZMQMessage(name="myname").json_bytes())
        self.assertNotIn("value", data)

        data = orjson.loads(SomeZMQMessage(name="myname", value=1).json_bytes())
        self.assertIn("value", data)
        self.assertEqual(1, data["value"])

        # to my understanding pydantic, openapi and jsonschema all do not agree how nullable but required
        # fields should correctly be handled / annotated. Currently our strategy is to use exclude_none=True
        # so null values are not exported, in an ideal world i would like to have value=None exported, but
        # it is currently not possible
        data = orjson.loads(SomeZMQMessage(name="myname", value=None).json_bytes())
        # self.assertIn("value", data)
        # self.assertEqual(None, data["value"])
        self.assertNotIn("value", data)
