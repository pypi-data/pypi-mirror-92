import logging
import os
import socket
import warnings
from types import SimpleNamespace
from unittest import TestCase

from openmodule import config
from openmodule.config import validate_config_module


class EnvTestCase(TestCase):
    initial_env: dict

    def env(self, value, key="t"):
        os.environ[key] = value

    def setUp(self) -> None:
        self.initial_env = os.environ.copy()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        os.environ.clear()
        os.environ.update(self.initial_env)


class ConfigTest(EnvTestCase):
    def test_int(self):
        self.env("1")
        self.assertEqual(1, config.int("t", 0))

        self.env("a")
        self.assertEqual(0, config.int("t", 0))

        self.env("0x16")
        self.assertEqual(0, config.int("t", 0))

        with self.assertRaises(AssertionError):
            config.int("t", 1.1)

    def test_float(self):
        self.env("1")
        self.assertEqual(1, config.float("t", 0))
        self.env("1.0")
        self.assertEqual(1, config.float("t", 0))
        self.env("1.1")
        self.assertEqual(1.1, config.float("t", 0))

        self.env("a")
        self.assertEqual(0, config.float("t", 0))

        self.env("0x16")
        self.assertEqual(0, config.float("t", 0))

        with self.assertRaises(AssertionError):
            config.float("t", "a")

    def test_str(self):
        self.env("1")
        self.assertEqual("1", config.string("t", "a"))

        self.env(" \"'1' \r\n\t")  # config.string strips unnecessary whitespace and quotes
        self.assertEqual("1", config.string("t", "a"))

        with self.assertRaises(AssertionError):
            config.string("t", 1.0)  # noqa

    def test_bool(self):
        self.env("1")
        self.assertTrue(config.bool("t", False))
        self.env("y")
        self.assertTrue(config.bool("t", False))
        self.env("Y")
        self.assertTrue(config.bool("t", False))
        self.env("t")
        self.assertTrue(config.bool("t", False))
        self.env("true")
        self.assertTrue(config.bool("t", False))
        self.env("yes")
        self.assertTrue(config.bool("t", False))

        # empty string is default value
        self.env("")
        self.assertTrue(config.bool("t", True))
        self.assertFalse(config.bool("t", False))

        with self.assertRaises(AssertionError):
            config.bool("t", "a")  # noqa

    def test_log_level(self):
        self.env("", "LOG_LEVEL")
        self.assertEqual(logging.INFO, config.log_level())  # info is the default value
        self.env("info", "LOG_LEVEL")
        self.assertEqual(logging.INFO, config.log_level())
        self.env("WARN", "LOG_LEVEL")
        self.assertEqual(logging.WARNING, config.log_level())
        self.env("ERROR", "LOG_LEVEL")
        self.assertEqual(logging.ERROR, config.log_level())
        self.env("CRITICAL", "LOG_LEVEL")
        self.assertEqual(logging.CRITICAL, config.log_level())
        self.env("VERBOSE", "LOG_LEVEL")
        self.assertEqual(logging.DEBUG, config.log_level())
        self.env("DEbUG", "LOG_LEVEL")
        self.assertEqual(logging.DEBUG, config.log_level())

    def test_version(self):
        # read version from env first
        self.env("1.0.0", "VERSION")
        self.assertEqual("1.0.0", config.version())

        # if it is not present, read it from VERSION file
        self.env("", "VERSION")
        try:
            with open("VERSION", "w") as f:
                f.write("1.0.0\n")
            self.assertEqual("1.0.0", config.version())
        finally:
            os.unlink("VERSION")

        # if we find nothing, version === "unknown"
        self.assertEqual("unknown", config.version())

    def test_resource(self):
        # no auth credentials set -> use hostname which is nice during development
        self.assertEqual(socket.gethostname(), config.resource())

        self.env("TEST123", "AUTH_RESOURCE")
        self.assertEqual("TEST123", config.resource())


class LegacyConfigSupportTest(EnvTestCase):
    def test_broker_pub(self):
        # nothing found -> defaults
        self.assertEqual("tcp://127.0.0.1:10200", config.broker_pub())

        # legacy configs
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_PUB_PORT")
        self.assertEqual("tcp://1.2.3.4:1234", config.broker_pub())

        # new configs overrule
        self.env("inproc://test-pub", "BROKER_PUB")
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_PUB_PORT")
        self.assertEqual("inproc://test-pub", config.broker_pub())

    def test_broker_sub(self):
        # nothing found -> defaults
        self.assertEqual("tcp://127.0.0.1:10100", config.broker_sub())

        # legacy configs
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_SUB_PORT")
        self.assertEqual("tcp://1.2.3.4:1234", config.broker_sub())

        # new configs overrule
        self.env("inproc://test-pub", "BROKER_SUB")
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_SUB_PORT")
        self.assertEqual("inproc://test-pub", config.broker_sub())

    def test_missing_keys_in_config_cause_assertion(self):
        fake_config = SimpleNamespace()
        fake_config.NAME = "test"
        with self.assertRaises(AssertionError):
            validate_config_module(fake_config)

    def test_legacy_broker_configs_cause_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            fake_config = SimpleNamespace()
            fake_config.NAME = "test"
            fake_config.RESOURCE = "test"
            fake_config.VERSION = "test"
            fake_config.BROKER_PUB_PORT = "10000"
            validate_config_module(fake_config)

            self.assertEqual(1, len(w))
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("BROKER_PUB", str(w[0].message))
