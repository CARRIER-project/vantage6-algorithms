from base64 import b64encode
from hashlib import sha512
from typing import List

import pandas as pd


def fixed_length_string(string: str, desired_length: int = 128):
    """
    Either truncate or padd a string with 'a' so that it is of the specified
    length.
    TODO: This is token from Chang's repo. Do we really want to support this or
        just enforce 128 length salts?
    Args:
        string (str): String to be processed
        desired_length (int): Desired length of the string
    """
    diff = desired_length - len(string)
    if diff > 0:
        string = string + ("a" * diff)
    elif diff < 0:
        string = string[:diff]
    return string


def salthash(salt, string):
    """
    Hash string using SHA 512 hashing with salt. Base64 encode resulting
    hash.

    Args:
        salt (str): (random) string of length 128
        string (str): arbitrary length string
    Returns:
        hashed 'salt + string'
    Raises:
        ValueError: if salt is not of length 128
    """
    if len(salt) != 128:
        raise ValueError('Salt must be 128 bytes long.')
    hashed = sha512((salt + string).encode('utf-8')).digest()
    return b64encode(hashed).decode('utf-8')


def encrypt_identifiers(df: pd.DataFrame, salt: str,
                        identifiers: List[str]) -> pd.DataFrame:
    """
    Join identifiers (i.e. columns identifying a record) and hash them to
    form an encrypted identifier. Drop original identifying columns.

    Args:
        df (pd.DataFrame): pandas dataframe
        salt (str): salt to be used when hashing
        identifiers (List(str)): column names of record identifiers

    Returns:
        (pd.DataFrame) with the column 'encrypted_identifier' instead of the
            original identifier columns.
    """
    def _hash_identifiers(row):
        try:
            identifier_values = row[identifiers]
        except KeyError as m:
            raise KeyError(f'One of the identifying variables is not found in '
                           f'the dataset, see original error: {m}')
        if any(pd.isna(identifier_values)):
            raise ValueError('One of the identifier values is NaN or None')
        joined_ids = ''.join(identifier_values.apply(str)).replace(' ', '')
        return salthash(salt, joined_ids)
    df['encrypted_identifier'] = df.apply(_hash_identifiers, axis=1)
    return df.drop(columns=identifiers)
