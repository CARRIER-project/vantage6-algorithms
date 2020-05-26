#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the vantage6-algorithms module.
"""
import pytest

from vantage6-algorithms import vantage6-algorithms


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


def test_vantage6-algorithms(an_object):
    assert an_object == {}
