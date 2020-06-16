from v6_carrier_py import master
from unittest.mock import MagicMock

ID = 1
COLUMN_NAMES = ['name1', 'name2']
TRIES = 1
MOCK_TASK = {'id': ID}


def test_column_names_returns_column_set():
    client = create_base_mock_client()
    client.get_results.return_value = [COLUMN_NAMES]

    result = master.column_names(client, None, {'tries': TRIES})

    target = set(COLUMN_NAMES)

    assert target == result


def test_master_node_excluded_from_task():
    my_organization_id = 1
    organization_ids = [1, 2, 3]
    client = create_base_mock_client()
    client.whoami.organization_id = my_organization_id
    client.get_organizations_in_my_collaboration.return_value = [{'id': i} for i in organization_ids]

    master.column_names(client, None, {'tries': TRIES})
    client.create_new_task.assert_called_once_with(input_={'method': 'column_names'}, organization_ids=[2, 3])


def create_base_mock_client():
    client = MagicMock()
    client.create_new_task.return_value = MOCK_TASK
    client.get_task.return_value = {'complete': True}
    client.get_results.return_value = [COLUMN_NAMES]

    return client()
