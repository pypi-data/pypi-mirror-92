import re
from argparse import ArgumentParser, Namespace

from pyppy.args import fill_arguments
from pyppy.conditions import condition, exp, and_
from pyppy.config import initialize_config, destroy_config
from pyppy.pipeline import step, Pipeline, PipelineModes
from pyppy.exc import IllegalStateException
from test.testcase import TestCase


class RoundTripTest(TestCase):

    def setUp(self) -> None:
        destroy_config()
        Pipeline.destroy()

    def tearDown(self) -> None:
        destroy_config()
        Pipeline.destroy()

    def test_decorator_stacking(self):
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")

        parser_sub1 = subparsers.add_parser('sub1')
        parser_sub1.add_argument('--sub1-tmp', type=int)

        parser_sub2 = subparsers.add_parser('sub2')
        parser_sub2.add_argument('--sub2-tmp', type=int)

        cli_args = ["sub1", "--sub1-tmp", "1"]
        initialize_config(parser.parse_args(cli_args))

        @step("tmp")
        @condition(exp(lambda c: c.command == "sub1"))
        @fill_arguments()
        def tmp1(sub1_tmp):
            return f"func1:{sub1_tmp}"

        @step("tmp")
        @condition(exp(lambda c: c.command == "sub2"))
        @fill_arguments()
        def tmp2(sub2_tmp):
            return f"func1:{sub2_tmp}"

        self.assertEqual(tmp1(), "func1:1")
        self.assertIsNone(tmp2())

        result = [r for r in Pipeline.run("tmp", mode=PipelineModes.GENERATOR_RETURNS)]
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "func1:1")
        self.assertIsNone(result[1][1])

    def test_inject_from_config(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp")
        @fill_arguments()
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        cli_args = ["--b", "b__"]
        initialize_config(parser.parse_args(cli_args))

        result = [r for r in Pipeline.run("tmp", mode=PipelineModes.GENERATOR_RETURNS)][0]
        self.assertEqual(result, ("tmp1", "func1:a_b__"))

    def test_inject_failure(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp")
        @fill_arguments()
        def tmp1(x, b="c"):
            return f"func1:{x}{b}"

        with self.assertRaises(IllegalStateException):
            initialize_config(parser.parse_args(["--b", "b__"]))

            result = [r for r in Pipeline.run("tmp", mode=PipelineModes.GENERATOR_RETURNS)][0]
            self.assertEqual(result, "func1:a_b__")

    def test_conditional_execution_1(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp", "first")
        @fill_arguments()
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        @step("tmp", "second")
        @condition(exp(a="_"))
        @fill_arguments()
        def tmp2():
            print("func2")
            return "func2"

        initialize_config(parser.parse_args(["--b", "b__"]))

        result = [r for r in Pipeline.run("tmp", mode=PipelineModes.GENERATOR_RETURNS)]
        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], ("first", "func1:a_b__"))
        self.assertEqual(result[1], ("second", None))

    def test_conditional_execution_2(self):
        parser = ArgumentParser()
        parser.add_argument("--a", default="a_")
        parser.add_argument("--b", default="b_")

        @step("tmp", "first")
        @fill_arguments()
        def tmp1(a, b="c"):
            return f"func1:{a}{b}"

        expression = and_(
            exp(a="a_"),
            exp(b="b__")
        )

        @step("tmp", "second")
        @condition(expression)
        def tmp2():
            print("func2")
            return "func2"

        initialize_config(parser.parse_args(["--b", "b__"]))

        result = [r for r in Pipeline.run("tmp", PipelineModes.GENERATOR_RETURNS)]
        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], ("first", "func1:a_b__"))
        self.assertEqual(result[1], ("second", "func2"))

    def test_get_executed_steps(self):
        namespace = Namespace()
        namespace.arg1 = "val1"
        namespace.arg2 = "not_val2"
        namespace.arg3 = "val3"

        initialize_config(namespace)

        @condition(exp(arg1="val1"))
        def tmp1():
            return f"1"

        @condition(exp(arg2="val2"))
        def tmp2():
            return f"2"

        @condition(exp(arg3="val3"))
        def tmp3():
            return f"3"

        Pipeline.create_pipeline("tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        steps = Pipeline.get_executed_steps("tmp")
        self.assertEqual(steps.executed, ["tmp-1", "tmp-3"])
        self.assertEqual(steps.not_executed, ["tmp-2"])

        str_steps = Pipeline.get_executed_steps("tmp", string_representation=True)
        self.assertEqual(re.sub(r"[\|\- +\n]", "", str_steps), "StepExecutedtmp1Xtmp2tmp3X")
