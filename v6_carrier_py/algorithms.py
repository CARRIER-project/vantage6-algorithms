import pandas as pd
from vantage6.tools.util import info


def RPC_column_names(data: pd.DataFrame, *args, **kwargs):
    """Column names

    List the names of the table columns
    """
    info("Retrieving column names")

    # what you return here is sent to the central server. So make sure
    # no privacy sensitive data is shared
    return data.columns.to_list()


def RPC_correlation_matrix(data: pd.DataFrame, *args, **kwargs):
    return data.corr()


def RPC_get_data(data: pd.DataFrame, *args, **kwargs):
    """
    Return the raw data.
    TODO: This function should not exist in the final version of the code! The data should be pseudonymized at the very
        least!

    """
    info(f'Returning raw data with {len(data)} records')
    return data


def RPC_count(data: pd.DataFrame, *args, **kwargs):
    """
    Count the number of rows in the result.

    :param data:
    :param args:
    :param kwargs:
    :return:
    """
    return len(data.index)
