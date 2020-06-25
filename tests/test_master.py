from sklearn import pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

from v6_carrier_py import master
from unittest.mock import MagicMock
import pytest
import pandas as pd

ID = 1
TRIES = 1
MOCK_TASK = {'id': ID}
IDENTIFIER_KEYS = ['GBAGeboorteJaar', 'GBAGeboorteMaand', 'GBAGeboorteDag', 'GBAGeslacht', 'GBAPostcode',
                   'GBAHuisnummer',
                   'GBAToev']
KEY_VALUES = [1987, 10, 30, 1, '1098ln', 11, 'b']
COLUMN1 = 'column1'
COLUMN2 = 'column2'

IRIS_DATASET = load_iris()


def test_column_names_returns_column_set():
    client = create_base_mock_client()
    client.get_results.return_value = [[COLUMN1], [COLUMN2]]

    result = master.column_names(client, None, tries=TRIES)

    target = {COLUMN1, COLUMN2}

    assert target == result


def test_column_names_master_node_excluded_from_task():
    my_organization_id = 1
    organization_ids = [1, 2, 3]
    client = create_base_mock_client()
    client.get_organizations_in_my_collaboration.return_value = [{'id': i} for i in organization_ids]

    master.column_names(client, None, tries=TRIES, exclude_orgs=[my_organization_id])
    client.create_new_task.assert_called_once_with(input_={'method': 'column_names'}, organization_ids=[2, 3])


def test_column_names_raise_exception_when_task_timeout():
    client = create_base_mock_client()
    client.get_task.return_value = {'complete': False}

    with pytest.raises(Exception):
        master.column_names(client, None, tries=TRIES)


def test_master_corr_matrix_is_combined_corr_matrix():
    client = create_base_mock_client()

    df1 = pd.DataFrame({'id': [1], COLUMN1: [123]})
    df2 = pd.DataFrame({'id': [1], COLUMN2: [321]})

    node_results = [df1, df2]
    client.get_results.return_value = node_results

    result = master.correlation_matrix(client, None, tries=TRIES, keys='id')
    target = pd.DataFrame({'id': [1], COLUMN1: [123], COLUMN2: [321]}).corr()

    pd.testing.assert_frame_equal(target, result)


def test_master_corr_matrix_joins_on_multiple_keys():
    client = create_base_mock_client()

    df1 = pd.DataFrame(data=[KEY_VALUES + [123]], columns=IDENTIFIER_KEYS + [COLUMN1])
    df2 = pd.DataFrame(data=[KEY_VALUES + [321]], columns=IDENTIFIER_KEYS + [COLUMN2])

    client.get_results.return_value = [df1, df2]

    target = pd.DataFrame(data=[KEY_VALUES + [123, 321]], columns=IDENTIFIER_KEYS + [COLUMN1, COLUMN2]).corr()
    result = master.correlation_matrix(client, None, keys=IDENTIFIER_KEYS, tries=TRIES)

    pd.testing.assert_frame_equal(target, result)


def test_correlation_matrix_if_no_keys_provided_infer_keys():
    client = create_base_mock_client()
    key_values = [1987, 10, 30, 1, '1098ln', 11, 'b']

    df1 = pd.DataFrame(data=[key_values + [123]], columns=IDENTIFIER_KEYS + [COLUMN1])
    df2 = pd.DataFrame(data=[key_values + [321]], columns=IDENTIFIER_KEYS + [COLUMN2])

    client.get_results.return_value = [df1, df2]

    target = pd.DataFrame(data=[key_values + [123, 321]], columns=IDENTIFIER_KEYS + [COLUMN1, COLUMN2]).corr()

    # This time no keys are specified, but it should still give the expected result
    result = master.correlation_matrix(client, None, tries=TRIES)

    pd.testing.assert_frame_equal(target, result)


def test_correlation_matrix_dont_mix_up_partly_matching_keys():
    client = create_base_mock_client()

    # Two different people with the same birth date
    person1 = [1987, 10, 30, 1, '1098ln', 11, 'b']
    person2 = [1987, 10, 30, 1, '1098ln', 12, '']

    data_left = [person1 + [1], person2 + [0]]
    data_right = [person1 + [1], person2 + [0]]

    pd_left = pd.DataFrame(data_left, columns=IDENTIFIER_KEYS + [COLUMN1])
    pd_right = pd.DataFrame(data_right, columns=IDENTIFIER_KEYS + [COLUMN2])

    client.get_results.return_value = [pd_left, pd_right]

    # If data is merged correctly, correlation between column1 and column2 should be 1, otherwise it is 0.5
    result = master.correlation_matrix(client, None, tries=TRIES)
    assert result[COLUMN1][COLUMN2] == 1


def test_train_model_runs_pipeline():
    # TODO: Remove test later
    pipe = pipeline.make_pipeline(StandardScaler(), GaussianNB(priors=None))
    feature_names = IRIS_DATASET['feature_names']
    data = pd.DataFrame(data=IRIS_DATASET['data'], columns=feature_names)
    data['y'] = IRIS_DATASET['target']

    client = create_base_mock_client()
    client.get_results.return_value = [data]
    result = master.train_model(client, None, pipe, feature_names, 'y')

    print(result)

    assert result is not None


def create_base_mock_client():
    client = MagicMock()
    client.create_new_task.return_value = MOCK_TASK
    client.get_task.return_value = {'complete': True}
    client.get_results.return_value = [COLUMN1, COLUMN2]

    return client()
