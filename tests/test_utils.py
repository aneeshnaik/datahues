import pytest
from datahues.utils import _check_valid_hex


###############################################################################
# Tests for _check_valid_hex function
###############################################################################

def test_valid_hex():
    """Valid hex codes should not raise an error."""
    _check_valid_hex("#FF0000")
    _check_valid_hex("#00FF00")
    _check_valid_hex("#0000FF")


@pytest.mark.parametrize("badhex", [123, True, None])
def test_invalid_hex_not_string(badhex):
    """Non-string input should raise ValueError."""
    with pytest.raises(ValueError, match="Hex must be a string"):
        _check_valid_hex(badhex)


def test_invalid_hex_no_hash():
    """Hex without '#' should raise ValueError."""
    with pytest.raises(ValueError, match="Hex must start with"):
        _check_valid_hex("FF0000")


@pytest.mark.parametrize("badhex", ["#FF00", "#FF00000"])
def test_invalid_hex_wrong_length(badhex):
    """Hex with wrong length should raise ValueError."""
    with pytest.raises(ValueError, match="7 characters long"):
        _check_valid_hex(badhex)


def test_invalid_hex_bad_characters():
    """Hex with invalid characters should raise ValueError."""
    with pytest.raises(ValueError, match="valid hexadecimal"):
        _check_valid_hex("#GGGGGG")


# TODO tests for _check_valid_rgb function
# TODO tests for _check_valid_xyz function
# TODO tests for _check_valid_lab function