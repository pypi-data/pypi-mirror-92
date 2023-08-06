from argparse import ArgumentParser, Namespace

from pyppy.conditions import condition, Exp, and_, or_
from pyppy.exc import ConditionRaisedException
from test.testcase import TestCase
from pyppy.config import initialize_config, destroy_config, config
from test.testing import fake_config

DEFAULT_ARG_DICT = {
    "arg1": "val1",
    "arg2": "val2",
    "arg3": "val3",
    "arg4": "val4"
}


class ConditionsTest(TestCase):

    def setUp(self) -> None:
        destroy_config()

    def test_single_condition_true(self):
        with fake_config(**DEFAULT_ARG_DICT):
            @condition(Exp(lambda c: c.arg1 == "val1"))
            def tmp():
                return "returned"

            self.assertTrue(tmp() == "returned")

    def test_single_condition_false(self):
        with fake_config(tmp1=1):
            @condition(Exp(lambda c: c.tmp1 == 2))
            def tmp():
                return "returned"

            with self.assertNotRaises(ConditionRaisedException):
                tmp()

            self.assertIsNone(tmp())

    def test_initialize_after(self):
        """
        Test if initialization works after defining
        a method with a condition.
        """

        namespace = Namespace()
        namespace.tmp1 = 1

        @condition(Exp(lambda c: c.tmp1 == 1))
        def tmp():
            return "returned"

        initialize_config(namespace)

        self.assertEqual(tmp(), "returned")

    def test_subparser_condition_wrong_order(self):
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        parser_sub1 = subparsers.add_parser('sub1')
        parser_sub1.add_argument('--sub1-tmp', type=int)

        parser_sub2 = subparsers.add_parser('sub2')
        parser_sub2.add_argument('--sub2-tmp', type=int)

        args = parser.parse_args(["sub1", "--sub1-tmp", "1"])
        initialize_config(args)
        self.assertEqual(config().sub1_tmp, 1)

        @condition(
            and_(
                Exp(lambda c: c.sub2_tmp == 2),
                Exp(lambda c: c.command == "sub2")
            )
        )
        def tmp1():
            return "returned"

        with self.assertRaises(ConditionRaisedException):
            tmp1()

    def test_subparser_condition_right_order(self):
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        parser_sub1 = subparsers.add_parser('sub1')
        parser_sub1.add_argument('--sub1-tmp', type=int)

        parser_sub2 = subparsers.add_parser('sub2')
        parser_sub2.add_argument('--sub2-tmp', type=int)

        args = parser.parse_args(["sub1", "--sub1-tmp", "1"])
        initialize_config(args)
        self.assertEqual(config().sub1_tmp, 1)

        @condition(
            and_(
                Exp(lambda c: c.command == "sub2"),
                Exp(lambda c: c.sub2_tmp == 2)
            )
        )
        def tmp2():
            return "returned"

        with self.assertNotRaises(AttributeError):
            tmp2()

        self.assertIsNone(tmp2())

    def test_single_exp(self):
        @condition(Exp(a="b"))
        def tmp():
            return "returned"

        initialize_config(Namespace())
        conf = config()
        conf._allow_overriding = True
        conf.a = "b"
        self.assertTrue(tmp() == "returned")

        conf.a = "c"
        self.assertIsNone(tmp())

    def test_nested_exp_1(self):
        with fake_config(a="b", d="e"):
            expression = and_(
                or_(
                    Exp(a="b"),
                    Exp(b="c")
                ),
                Exp(d="e")
            )

            @condition(expression)
            def tmp():
                return "returned"

            self.assertTrue(tmp() == "returned")

    def test_nested_exp_2(self):
        with fake_config(b="c", d="e"):
            expression = and_(
                or_(
                    Exp(a="b"),
                    Exp(b="c")
                ),
                Exp(d="e")
            )

            @condition(expression)
            def tmp():
                return "returned"

            self.assertTrue(tmp() == "returned")

    def test_nested_exp_3(self):
        with fake_config(a="b", b="c"):
            expression = and_(
                or_(
                    Exp(a="b"),
                    Exp(b="c")
                ),
                Exp(d="e")
            )

            @condition(expression)
            def tmp():
                return "returned"

            self.assertIsNone(tmp())

    def test_nested_exp_4(self):
        with fake_config(d="e"):
            expression = and_(
                or_(
                    Exp(a="b"),
                    Exp(b="c")
                ),
                Exp(d="e")
            )

            @condition(expression)
            def tmp():
                return "returned"

            self.assertIsNone(tmp())

    def test_expressions(self):
        with fake_config(a="b"):

            expression = or_(
                Exp(a="b"),
                Exp(b="c")
            )

            self.assertTrue(expression())
            delattr(config(), "a")
            self.assertFalse(expression())
