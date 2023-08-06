# -*- coding: utf-8 -*-

import pytest

from ml_flow_client.skeleton import fib

__author__ = "Sven Haadem"
__copyright__ = "Sven Haadem"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
