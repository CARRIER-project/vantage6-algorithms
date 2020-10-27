import pickle
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from v6_carrier_py import wrapper

MOCK_MODULE = 'mock_module'
MOCK_TOKEN = 'token'
MOCK_ENDPOINT = 'http://example.org'


@patch('v6_carrier_py.wrapper.dispact_rpc')
@patch('v6_carrier_py.wrapper.os')
def test_wrapper_passes_dataframe(os: MagicMock, dispact_rpc: MagicMock, tmp_path: Path):
    input_file = tmp_path / 'input_file.pkl'
    token_file = tmp_path / 'token.txt'
    output_file = tmp_path / 'output.pkl'

    environ = {'INPUT_FILE': str(input_file),
               'TOKEN_FILE': str(token_file),
               'DATABASE_URI': MOCK_ENDPOINT,
               'OUTPUT_FILE': str(output_file)}

    os.environ = environ

    input_args = {'query': 'select *'}

    with input_file.open('wb') as f:
        pickle.dump(input_args, f)

    with token_file.open('w') as f:
        f.write(MOCK_TOKEN)

    dispact_rpc.return_value = pd.DataFrame()

    wrapper.sparql_wrapper(MOCK_MODULE)

    dispact_rpc.assert_called_once()
    pd.testing.assert_frame_equal(pd.DataFrame(), dispact_rpc.call_args[0][0])

