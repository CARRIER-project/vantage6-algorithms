from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from sklearn import pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler

from v6_carrier_py import master

ID = 1
TRIES = 1
MOCK_TASK = {'id': ID}
IDENTIFIER_KEYS = ['GBAGeboorteJaar', 'GBAGeboorteMaand', 'GBAGeboorteDag', 'GBAGeslacht', 'GBAPostcode',
                   'GBAHuisnummer', 'GBAToev']
KEY_VALUES = [1987, 10, 30, 1, '1098ln', 11, 'b']
COLUMN1 = 'column1'
COLUMN2 = 'column2'

DATASET = 'tests/resources/joined_data.csv'

# Arbitrary features
FEATURES = ['height', 'weight', 'bmi', 'Age', 'n_smokingcat4', 'WOZ', 'N_ALCOHOL_CAT',
            'ZVWKOPHOOGFACTOR_2010', 'ZVWKHUISARTS_2010', 'ZVWKFARMACIE_2010', 'ZVWKZIEKENHUIS_2010',
            'ZVWKPARAMEDISCH_2010', 'ZVWKZIEKENVERVOER_2010',
            'ZVWKBUITENLAND_2010', 'ZVWKOVERIG_2010', 'ZVWKEERSTELIJNSPSYCHO_2010', 'ZVWKGGZ_2010',
            'ZVWKHULPMIDDEL_2010', 'ZVWKOPHOOGFACTOR_2011', 'ZVWKHUISARTS_2011']
TARGET = 'N_CVD'


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

    with patch('v6_carrier_py.master.MIN_RECORDS', 0):
        result = master.correlation_matrix(client, None, tries=TRIES, keys='id')
        target = pd.DataFrame({'id': [1], COLUMN1: [123], COLUMN2: [321]}).corr()

        pd.testing.assert_frame_equal(target, result)


def test_master_corr_matrix_joins_on_multiple_keys():
    client = create_base_mock_client()

    df1 = pd.DataFrame(data=[KEY_VALUES + [123]], columns=IDENTIFIER_KEYS + [COLUMN1])
    df2 = pd.DataFrame(data=[KEY_VALUES + [321]], columns=IDENTIFIER_KEYS + [COLUMN2])

    client.get_results.return_value = [df1, df2]

    target = pd.DataFrame(data=[KEY_VALUES + [123, 321]], columns=IDENTIFIER_KEYS + [COLUMN1, COLUMN2]).corr()

    with patch('v6_carrier_py.master.MIN_RECORDS', 0):
        result = master.correlation_matrix(client, None, keys=IDENTIFIER_KEYS, tries=TRIES)

        pd.testing.assert_frame_equal(target, result)


def test_correlation_matrix_if_no_keys_provided_infer_keys():
    client = create_base_mock_client()
    key_values = [1987, 10, 30, 1, '1098ln', 11, 'b']

    df1 = pd.DataFrame(data=[key_values + [123]], columns=IDENTIFIER_KEYS + [COLUMN1])
    df2 = pd.DataFrame(data=[key_values + [321]], columns=IDENTIFIER_KEYS + [COLUMN2])

    client.get_results.return_value = [df1, df2]

    target = pd.DataFrame(data=[key_values + [123, 321]], columns=IDENTIFIER_KEYS + [COLUMN1, COLUMN2]).corr()

    with patch('v6_carrier_py.master.MIN_RECORDS', 0):
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

    with patch('v6_carrier_py.master.MIN_RECORDS', 0):
        # If data is merged correctly, correlation between column1 and column2 should be 1, otherwise it is 0.5
        result = master.correlation_matrix(client, None, tries=TRIES)
        assert result[COLUMN1][COLUMN2] == 1


def test_train_model_accepts_dataset():
    dataset = load_dataset()

    pipe = pipeline.make_pipeline(StandardScaler(), GaussianNB(priors=None))
    mock_pipeline = MagicMock()
    mock_pipeline.reconstruct_pipeline.return_value = pipe
    client = create_base_mock_client()
    client.get_results.return_value = [dataset]

    with patch('v6_carrier_py.master.pipeline', mock_pipeline), patch('v6_carrier_py.master.MIN_RECORDS', 0):
        result = master.fit_pipeline(client, None, pipe, FEATURES, TARGET, IDENTIFIER_KEYS)

        assert result is not None


def create_base_mock_client():
    client = MagicMock()
    client.create_new_task.return_value = MOCK_TASK
    client.get_task.return_value = {'complete': True}
    client.get_results.return_value = [COLUMN1, COLUMN2]

    return client()


def load_dataset(path=DATASET):
    return pd.read_csv(path)
