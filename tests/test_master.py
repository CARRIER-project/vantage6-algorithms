from v6_carrier_py import master
from unittest.mock import MagicMock
import pytest
import pandas as pd

ID = 1
COLUMN_NAMES = ['name1', 'name2']
TRIES = 1
MOCK_TASK = {'id': ID}
KEYS = ['GBAGeboorteJaar', 'GBAGeboorteMaand', 'GBAGeboorteDag', 'GBAGeslacht', 'GBAPostcode', 'GBAHuisnummer',
        'GBAToev']
KEY_VALUES = [1987, 10, 30, 1, '1098ln', 11, 'b']


def test_column_names_returns_column_set():
    client = create_base_mock_client()
    client.get_results.return_value = [COLUMN_NAMES]

    result = master.column_names(client, None, tries=TRIES)

    target = set(COLUMN_NAMES)

    assert target == result


def test_master_node_excluded_from_task():
    my_organization_id = 1
    organization_ids = [1, 2, 3]
    client = create_base_mock_client()
    client.get_organizations_in_my_collaboration.return_value = [{'id': i} for i in organization_ids]

    master.column_names(client, None, tries=TRIES, exclude_orgs=[my_organization_id])
    client.create_new_task.assert_called_once_with(input_={'method': 'column_names'}, organization_ids=[2, 3])


def test_raise_exception_when_task_timeout():
    client = create_base_mock_client()
    client.get_task.return_value = {'complete': False}

    with pytest.raises(Exception):
        master.column_names(client, None, tries=TRIES)


def test_master_corr_matrix_is_combined_corr_matrix():
    client = create_base_mock_client()

    df1 = pd.DataFrame({'id': [1], 'column1': [123]})
    df2 = pd.DataFrame({'id': [1], 'column2': [321]})

    node_results = [df1, df2]
    client.get_results.return_value = node_results

    result = master.correlation_matrix(client, None, tries=TRIES, keys='id')
    target = pd.DataFrame({'id': [1], 'column1': [123], 'column2': [321]}).corr()

    pd.testing.assert_frame_equal(target, result)


def test_master_corr_matrix_joins_on_multiple_keys():
    client = create_base_mock_client()

    df1 = pd.DataFrame(data=[KEY_VALUES + [123]], columns=KEYS + ['column1'])
    df2 = pd.DataFrame(data=[KEY_VALUES + [321]], columns=KEYS + ['column2'])

    client.get_results.return_value = [df1, df2]

    target = pd.DataFrame(data=[KEY_VALUES + [123, 321]], columns=KEYS + ['column1', 'column2']).corr()
    result = master.correlation_matrix(client, None, keys=KEYS, tries=TRIES)

    pd.testing.assert_frame_equal(target, result)


def if_no_keys_provided_infer_keys():
    keys = ['GBAGeboorteJaar', 'GBAGeboorteMaand', 'GBAGeboorteDag', 'GBAGeslacht', 'GBAPostcode', 'GBAHuisnummer',
            'GBAToev']
    client = create_base_mock_client()
    key_values = [1987, 10, 30, 1, '1098ln', 11, 'b']

    df1 = pd.DataFrame(data=[key_values + [123]], columns=keys + ['column1'])
    df2 = pd.DataFrame(data=[key_values + [321]], columns=keys + ['column2'])

    client.get_results.return_value = [df1, df2]

    target = pd.DataFrame(data=[key_values + [123, 321]], columns=keys + ['column1', 'column2']).corr()

    # This time no keys are specified, but it should still give the expected result
    result = master.correlation_matrix(client, None, tries=TRIES)

    pd.testing.assert_frame_equal(target, result)


def create_base_mock_client():
    client = MagicMock()
    client.create_new_task.return_value = MOCK_TASK
    client.get_task.return_value = {'complete': True}
    client.get_results.return_value = [COLUMN_NAMES]

    return client()
