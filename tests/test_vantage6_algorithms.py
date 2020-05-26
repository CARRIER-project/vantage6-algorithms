#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the vantage6_algorithms module.
"""
import pytest

from vantage6_algorithms import vantage6_algorithms


def test_something():
    assert True


def test_with_error():
    with pytest.raises(ValueError):
        # Do something that raises a ValueError
        raise(ValueError)


# Fixture example
@pytest.fixture
def an_object():
    return {}


def test_vantage6_algorithms(an_object):
    assert an_object == {}
