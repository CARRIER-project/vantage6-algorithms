from v6_carrier_py import master
from unittest.mock import MagicMock
import pytest
import pandas as pd

ID = 1
COLUMN_NAMES = ['name1', 'name2']
TRIES = 1
MOCK_TASK = {'id': ID}


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

    result = master.correlation_matrix(client, None, tries=TRIES, key='id')
    target = pd.DataFrame({'id': [1], 'column1': [123], 'column2': [321]}).corr()

    pd.testing.assert_frame_equal(target, result)


def create_base_mock_client():
    client = MagicMock()
    client.create_new_task.return_value = MOCK_TASK
    client.get_task.return_value = {'complete': True}
    client.get_results.return_value = [COLUMN_NAMES]

    return client()
