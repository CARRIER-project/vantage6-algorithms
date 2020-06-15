from v6_carrier_py import algorithms
import pandas as pd

DATA = pd.DataFrame(data=[[1, 2], [3, 4]], columns=['column1', 'column2'])


def test_column_names_returns_names():
    result = algorithms.RPC_column_names(DATA)

    assert result == ['column1', 'column2']
