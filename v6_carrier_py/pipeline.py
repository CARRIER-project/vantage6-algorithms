from typing import Dict
from collections import defaultdict
from sklearn.pipeline import Pipeline, make_pipeline
from . import steps


def reconstruct_pipeline(pipe: Pipeline):
    pipeline_steps = _reconstruct_pipeline_steps(pipe)

    return make_pipeline(*pipeline_steps)


def _reconstruct_pipeline_steps(pipe: Pipeline):
    params = pipe.get_params()

    # Ignore the parameters that are not related to a specific step
    step_params = {k: v for k, v in params.items() if '__' in k}
    step_params = _convert_step_params(step_params)

    for name, step in pipe.steps:
        class_name = type(step).__name__
        steps.get_step_class(class_name)

        params = step_params.get(name, {})

        step_class = steps.get_step_class(class_name)
        step = step_class(**params)

        yield step


def get_step_params(params: Dict[str, any]) -> Dict[str, any]:
    return {k: v for k, v in params.items() if '__' in k}


def _convert_step_params(step_params):
    step_params = defaultdict(dict)

    for k, v in step_params.items():
        step_name, param = _split_step_param(k)
        step_params[step_name][param] = v

    return step_params


def _split_step_param(k):
    step_name, param = tuple(k.split('__', maxsplit=1))

    return step_name, param
