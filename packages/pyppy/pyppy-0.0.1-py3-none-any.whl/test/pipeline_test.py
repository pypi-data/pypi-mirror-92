import io
import re
import sys

from pyppy.pipeline import step, Pipeline, PipelineModes
from pyppy.exc import MissingPipelineException, PipelineAlreadyExistsException
from test.testcase import TestCase


class PipelineTest(TestCase):

    def setUp(self) -> None:
        Pipeline.destroy()

    def tearDown(self) -> None:
        Pipeline.destroy()

    def test_register_steps(self):
        @step("tmp")
        def tmp1():
            pass

        @step("tmp")
        def tmp2():
            pass

        @step("hurz")
        def hurz1():
            pass

        @step("hurz")
        def hurz2():
            pass

        steps = Pipeline.pipelines

        self.assertTrue("tmp" in steps)
        self.assertTrue(len(steps["tmp"]) == 2)
        self.assertTrue("tmp1" in str(steps["tmp"][0]))
        self.assertTrue("tmp2" in str(steps["tmp"][1]))

        self.assertTrue("hurz" in steps)
        self.assertTrue(len(steps["hurz"]) == 2)
        self.assertTrue("hurz1" in str(steps["hurz"][0]))
        self.assertTrue("hurz2" in str(steps["hurz"][1]))

    def test_run_pipeline(self):
        @step("tmp", "first")
        def tmp1():
            print("func1")
            return "func1"

        @step("tmp", "second")
        def tmp2():
            print("func2")
            return "func2"

        steps = Pipeline.pipelines

        self.assertTrue("tmp" in steps)
        self.assertTrue(len(steps["tmp"]) == 2)
        self.assertTrue("tmp1" in str(steps["tmp"][0]))
        self.assertTrue("tmp2" in str(steps["tmp"][1]))

        # temporarily redirect stdout
        old_stdout = sys.stdout
        sys.stdout = tmp_stdout = io.StringIO()
        Pipeline.run("tmp")
        sys.stdout = old_stdout
        self.assertEqual(
            re.sub(r"\s+", "", tmp_stdout.getvalue()),
            "func1func2",
        )

        with self.assertRaises(MissingPipelineException):
            Pipeline.run("ahsjdhfjaklsdf")

        results = [r for r in Pipeline.run("tmp", mode=PipelineModes.GENERATOR_RETURNS)]
        self.assertTrue(len(results) == 2)
        self.assertTrue(results[0] == ("first", "func1"))
        self.assertTrue(results[1] == ("second", "func2"))

    def test_create_pipeline_from_iterable(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        result = [r for r in Pipeline.run("iter-tmp", PipelineModes.GENERATOR_RETURNS)]

        self.assertTrue(len(result) == 3)
        self.assertEqual(result[0][1], "1")
        self.assertEqual(result[1][1], "2")
        self.assertEqual(result[2][1], "3")

    def test_pipeline_dict_results(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        result = dict([r for r in Pipeline.run("iter-tmp", PipelineModes.GENERATOR_RETURNS)])

        self.assertTrue(len(result) == 3)
        self.assertEqual(result["tmp-1"], "1")
        self.assertEqual(result["tmp-2"], "2")
        self.assertEqual(result["tmp-3"], "3")

    def test_pipeline_already_exists(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("tmp", [("tmp-1", tmp1)])

        with self.assertRaises(PipelineAlreadyExistsException):
            Pipeline.create_pipeline("tmp", [("tmp-2", tmp2)])

        self.assertTrue(len(Pipeline.pipelines["tmp"]) == 1)

        with self.assertRaises(PipelineAlreadyExistsException):
            Pipeline.create_pipeline("tmp", [("tmp-3", tmp3)], extend=False)

        self.assertTrue(len(Pipeline.pipelines["tmp"]) == 1)

        Pipeline.create_pipeline("tmp", [("tmp-2", tmp2), ("tmp-3", tmp3)], extend=True)
        self.assertTrue(len(Pipeline.pipelines["tmp"]) == 3)

        result = dict(Pipeline.run("tmp", mode=PipelineModes.GENERATOR_RETURNS))
        self.assertEqual(result["tmp-1"], "1")
        self.assertEqual(result["tmp-2"], "2")
        self.assertEqual(result["tmp-3"], "3")

    def test_pipeline_modes(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        no_result = Pipeline.run("iter-tmp", mode=PipelineModes.NO_RETURNS)
        self.assertIsNone(no_result)

        generator_result = Pipeline.run("iter-tmp", mode=PipelineModes.GENERATOR_RETURNS)
        self.assertEqual(next(generator_result), ("tmp-1", "1"))
        self.assertEqual(next(generator_result), ("tmp-2", "2"))
        self.assertEqual(next(generator_result), ("tmp-3", "3"))

        with self.assertRaises(StopIteration):
            next(generator_result)

        all_result = Pipeline.run("iter-tmp", mode=PipelineModes.ALL_RETURNS)
        self.assertEqual(all_result, {
            "tmp-1": "1",
            "tmp-2": "2",
            "tmp-3": "3"
        })

    def test_get_executed_steps_not_raises_when_no_condition(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])
        with self.assertNotRaises(AttributeError):
            Pipeline.get_executed_steps("iter-tmp")

    def test_get_executed_steps(self):
        def tmp1():
            return f"1"

        def tmp2():
            return f"2"

        def tmp3():
            return f"3"

        Pipeline.create_pipeline("iter-tmp", [
            ("tmp-1", tmp1),
            ("tmp-2", tmp2),
            ("tmp-3", tmp3)
        ])

        steps = Pipeline.get_executed_steps("iter-tmp")
        self.assertEqual(steps.executed, ["tmp-1", "tmp-2", "tmp-3"])

