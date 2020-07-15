from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNetCV
from v6_carrier_py import pipeline
import pytest


def test_reconstruct_pipeline_reconstructs_equal_pipeline():
    pipe = make_pipeline(LinearRegression())
    reconstructed = pipeline.reconstruct_pipeline(pipe)

    assert pipe is not reconstructed

    # Just comparing the dict will fail because the step objects are not equal (they are two separate instances)
    assert str(pipe.get_params()) == str(reconstructed.get_params())


def test_reconstruct_pipeline_fails_on_forbidden_steps():
    # Some random model
    pipe = make_pipeline(ElasticNetCV())

    with pytest.raises(Exception):
        pipeline.reconstruct_pipeline(pipe)
