"""Dummy module."""
import sys
from os import getcwd
from unittest.mock import Mock

import pytest


def dummy_function() -> None:
    """Do stuff."""
    from math import sin
    
    sys.version_info
    getcwd()
    Mock()
    pytest.approx(sin(0.1))
    return None
