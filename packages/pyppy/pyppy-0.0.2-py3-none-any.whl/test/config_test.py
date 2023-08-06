from argparse import ArgumentParser, Namespace

from pyppy.config import initialize_config, config, destroy_config
from pyppy.exc import ConfigAlreadyInitializedException
from test.testcase import TestCase


class ContainerTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_config(self):
        namespace = Namespace()
        namespace.tmp1 = "val1"
        namespace.tmp2 = 2

        initialize_config(namespace)
        conf = config()

        self.assertEqual(conf.tmp1, "val1")
        self.assertEqual(conf.tmp2, 2)

    def test_config_already_initialized(self):
        namespace = Namespace()
        namespace.tmp = "tmp"
        initialize_config(namespace)

        with self.assertRaises(ConfigAlreadyInitializedException):
            initialize_config(Namespace())

        self.assertEqual(namespace, config())

    def test_destroy_config(self):
        initialize_config(Namespace())
        conf = config()

        with self.assertRaises(AttributeError):
            conf.tmp

        destroy_config()

        parser2 = ArgumentParser()
        parser2.add_argument("--tmp5", type=str)
        parser2.add_argument("--tmp6", type=int)

        cli_args3 = ["--tmp5", "val5", "--tmp6", "6"]
        args3 = parser2.parse_args(cli_args3)
        initialize_config(args3)
        conf3 = config()

        self.assertNotEqual(conf3, conf)
        self.assertEqual(conf3.tmp5, "val5")
        self.assertEqual(conf3.tmp6, 6)

        with self.assertRaises(AttributeError):
            config().tmp1

        with self.assertRaises(AttributeError):
            config().tmp2