from v6_carrier_py import master
from unittest.mock import MagicMock

ID = 1
COLUMN_NAMES = ['name1', 'name2']
TRIES = 1


def test_column_names_returns_column_set():
    client = MagicMock()
    mock_task = {'id': ID}
    client.create_new_task.return_value = mock_task
    client.get_task.return_value = {'complete': True}
    client.get_results.return_value = [COLUMN_NAMES]

    result = master.column_names(client, {'tries': TRIES})

    target = set(COLUMN_NAMES)

    assert target == result
