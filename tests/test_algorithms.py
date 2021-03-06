from v6_carrier_py import algorithms
import pandas as pd

DATA = pd.DataFrame(data=[[1, 2], [3, 4]], columns=['column1', 'column2'])


def test_column_names_returns_names():
    result = algorithms.RPC_column_names(DATA)

    assert result == ['column1', 'column2']


def test_corr_matrix_creates_corr_matrix():
    result = algorithms.RPC_correlation_matrix(DATA)

    pd.testing.assert_frame_equal(DATA.corr(), result)


def test_get_data_returns_raw_data():
    result = algorithms.RPC_get_data(DATA)

    pd.testing.assert_frame_equal(DATA, result)
