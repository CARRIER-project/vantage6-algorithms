import pytest

from v6_carrier_py.encryption import salthash, encrypt_identifiers
import pandas as pd
import numpy as np


def test_salthash():
    salt = 'a' * 128
    string = 'hash me please'
    result = salthash(salt, string)
    assert result == 'EQ2Fczw0MVu0zqH30I0Vffbkga7SJO9tmnWjU2ZNf9gJeHa' \
                     'EETF9wJY13YPqdhsVwSMK1v+zVYYB6cgjDjHIjA=='


class TestEncryptIdentifiers:
    test_df = pd.DataFrame.from_dict({
        'identifier1': ['a', 'b'],
        'identifier2': ['c', 'd'],
        'value1': [1, 2]
    })
    test_identifiers = ['identifier1', 'identifier2']
    test_salt = 'a' * 128

    def test_encrypt_identifiers(self):
        result_df = encrypt_identifiers(self.test_df, self.test_salt,
                                        identifiers=self.test_identifiers)
        for identifier in self.test_identifiers:
            assert identifier not in result_df
        assert 'encrypted_identifier' in result_df

    def test_encrypt_identifiers_wrong_identifiers(self):
        test_wrong_identifiers = ['wrong_variable']
        with pytest.raises(KeyError):
            encrypt_identifiers(self.test_df, self.test_salt,
                                identifiers=test_wrong_identifiers)

    def test_encrypt_identifiers_null_values(self):
        test_df = self.test_df.copy()
        test_df['identifier1'] = np.nan
        with pytest.raises(ValueError):
            encrypt_identifiers(test_df, self.test_salt,
                                identifiers=self.test_identifiers)
