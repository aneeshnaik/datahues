"""Tests for ramp module."""
import pytest
from datahues.ramp import _check_valid_hex


def test_valid_hex():
    """Valid hex codes should not raise an error."""
    _check_valid_hex("#FF0000")
    _check_valid_hex("#00FF00")
    _check_valid_hex("#0000FF")


def test_invalid_hex_not_string():
    """Non-string input should raise ValueError."""
    with pytest.raises(ValueError, match="Hex must be a string"):
        _check_valid_hex(123)


def test_invalid_hex_no_hash():
    """Hex without '#' should raise ValueError."""
    with pytest.raises(ValueError, match="Hex must start with"):
        _check_valid_hex("FF0000")
