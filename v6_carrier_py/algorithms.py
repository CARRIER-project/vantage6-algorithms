import pandas as pd
from vantage6.tools.util import info
from .encryption import encrypt_identifiers

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


def RPC_get_pseudonimized_data(data: pd.DataFrame, identifying_fields, *args, **kwargs):
    """
    Return pseudonimized data.

    TODO: Identifying fields depend on the data at the data station. These fields could maybe be configured at the data
        station.
    """

    encrypt_identifiers()

    return data
