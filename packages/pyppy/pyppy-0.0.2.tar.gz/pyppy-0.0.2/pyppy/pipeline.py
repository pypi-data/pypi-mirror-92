from collections import namedtuple
from enum import Enum

from tabulate import tabulate

from pyppy.exc import MissingPipelineException, PipelineAlreadyExistsException


class PipelineModes(str, Enum):

    NO_RETURNS = "no_return"
    GENERATOR_RETURNS = "generator"
    ALL_RETURNS = "all_returns"


_Step = namedtuple('Step', ['name', 'func'])


def step(pipeline_name, step_name=None):
    def decorator(func):
        if not step_name:
            inner_step_name = func.__name__
        else:
            inner_step_name = step_name

        Pipeline.pipelines.setdefault(
            pipeline_name, []
        ).append(_Step(inner_step_name, func))

        return func
    return decorator


class Pipeline:

    pipelines = {}

    @staticmethod
    def _pipeline_exists(pipeline_name):
        if pipeline_name in Pipeline.pipelines:
            return True
        else:
            return False

    @staticmethod
    def run(pipeline_name, mode=PipelineModes.NO_RETURNS):
        if not Pipeline._pipeline_exists(pipeline_name):
            raise MissingPipelineException((
                f"Pipeline with name {pipeline_name} does "
                f"not exist!"
            ))

        if mode == PipelineModes.NO_RETURNS:
            for step in Pipeline.pipelines[pipeline_name]:
                step.func()
        elif mode == PipelineModes.ALL_RETURNS:
            result = []
            for step in Pipeline.pipelines[pipeline_name]:
                result.append((step.name, step.func()))
            return dict(result)
        elif mode == PipelineModes.GENERATOR_RETURNS:
            def generator_returns():
                for step in Pipeline.pipelines[pipeline_name]:
                    yield step.name, step.func()
            return generator_returns()

    @staticmethod
    def destroy(pipeline_name=None):
        if not pipeline_name:
            Pipeline.pipelines = {}
        else:
            Pipeline.pipelines.pop(pipeline_name, None)

    @staticmethod
    def create_pipeline(pipeline_name, iterable_of_tuples, extend=False):
        if Pipeline._pipeline_exists(pipeline_name) and not extend:
            raise PipelineAlreadyExistsException((
                f"Pipeline with name {pipeline_name} already exists!"
            ))
        for item in iterable_of_tuples:
            Pipeline.pipelines.setdefault(
                pipeline_name, []
            ).append(_Step(*item))

    @staticmethod
    def get_executed_steps(pipeline_name, string_representation=False):
        if not Pipeline._pipeline_exists(pipeline_name):
            raise MissingPipelineException((
                f"Pipeline with name {pipeline_name} does "
                f"not exist!"
            ))

        executed_steps = []
        not_executed_steps = []

        for step in Pipeline.pipelines[pipeline_name]:
            if hasattr(step.func, "exp"):
                if step.func.exp():
                    executed_steps.append(step.name)
                else:
                    not_executed_steps.append(step.name)
            else:
                executed_steps.append(step.name)

        if string_representation:
            out = []
            for step in Pipeline.pipelines[pipeline_name]:
                if step.name in executed_steps:
                    out.append([step.name, "X"])
                else:
                    out.append([step.name, "-"])
            return tabulate(out, headers=["Step", 'Executed'],
                            tablefmt='orgtbl')

        ExecutedSteps = namedtuple("ExecutedSteps", ("executed", "not_executed"))
        return ExecutedSteps(executed_steps, not_executed_steps)
