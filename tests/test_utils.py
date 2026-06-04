import pytest
import numpy as np
from datahues.utils import (
    _check_valid_hex, _check_valid_rgb, _check_valid_xyz, _check_valid_lab
)


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


###############################################################################
# Tests for _check_valid_rgb function
###############################################################################


def test_valid_rgb():
    """Valid RGB arrays should not raise an error."""
    _check_valid_rgb(np.array([0.0, 0.5, 1.0]))
    _check_valid_rgb(np.array([1.0, 1.0, 1.0]))
    _check_valid_rgb(np.array([0.0, 0.0, 0.0]))


def test_invalid_rgb_not_array():
    """Non-array input should raise ValueError."""
    with pytest.raises(ValueError, match="RGB must be a numpy array"):
        _check_valid_rgb([0.0, 0.5, 1.0])


def test_invalid_rgb_wrong_shape():
    """RGB arrays with wrong shape should raise ValueError."""
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_rgb(np.array([0.0, 0.5]))
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_rgb(np.array([0.0, 0.5, 1.0, 0.5]))
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_rgb(np.array([[0.0, 0.5, 1.0]]))


def test_invalid_rgb_out_of_range():
    """RGB values outside [0.0, 1.0] should raise ValueError."""
    with pytest.raises(ValueError, match="RGB values must be in"):
        _check_valid_rgb(np.array([-0.1, 0.5, 1.0]))
    with pytest.raises(ValueError, match="RGB values must be in"):
        _check_valid_rgb(np.array([0.0, 0.5, 1.1]))


def test_invalid_rgb_non_numeric():
    """RGB arrays with non-numeric values should raise ValueError."""
    with pytest.raises(ValueError, match="RGB must have a numeric dtype"):
        _check_valid_rgb(np.array([0.0, "0.5", 1.0]))
    with pytest.raises(ValueError, match="RGB must have a numeric dtype"):
        _check_valid_rgb(np.array([0.0, None, 1.0]))


###############################################################################
# Tests for _check_valid_xyz function
###############################################################################


def test_valid_xyz():
    """Valid XYZ arrays should not raise an error."""
    _check_valid_xyz(np.array([0.0, 0.5, 1.0]))
    _check_valid_xyz(np.array([1.5, 1.0, 1.0]))
    _check_valid_xyz(np.array([0.0, 0.0, 0.0]))


def test_invalid_xyz_not_array():
    """Non-array input should raise ValueError."""
    with pytest.raises(ValueError, match="XYZ must be a numpy array"):
        _check_valid_xyz([0.0, 0.5, 1.0])


def test_invalid_xyz_wrong_shape():
    """XYZ arrays with wrong shape should raise ValueError."""
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_xyz(np.array([0.0, 0.5]))
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_xyz(np.array([0.0, 0.5, 1.0, 0.5]))
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_xyz(np.array([[0.0, 0.5, 1.0]]))


def test_invalid_xyz_negative_values():
    """XYZ values outside [0.0, ∞) should raise ValueError."""
    with pytest.raises(ValueError, match="XYZ values must be non-negative"):
        _check_valid_xyz(np.array([-0.1, 0.5, 1.0]))
    with pytest.raises(ValueError, match="XYZ values must be non-negative"):
        _check_valid_xyz(np.array([0.0, -0.5, 1.0]))
    with pytest.raises(ValueError, match="XYZ values must be non-negative"):
        _check_valid_xyz(np.array([0.0, 0.5, -1.0]))


def test_invalid_xyz_non_numeric():
    """XYZ arrays with non-numeric values should raise ValueError."""
    with pytest.raises(ValueError, match="XYZ must have a numeric dtype"):
        _check_valid_xyz(np.array([0.0, "0.5", 1.0]))
    with pytest.raises(ValueError, match="XYZ must have a numeric dtype"):
        _check_valid_xyz(np.array([0.0, None, 1.0]))


###############################################################################
# Tests for _check_valid_lab function
###############################################################################


def test_valid_lab():
    """Valid Oklab arrays should not raise an error."""
    _check_valid_lab(np.array([0.0, 0.5, 1.0]))
    _check_valid_lab(np.array([1.0, -0.5, 0.5]))
    _check_valid_lab(np.array([0.5, 0.0, -0.5]))


def test_invalid_lab_not_array():
    """Non-array input should raise ValueError."""
    with pytest.raises(ValueError, match="Oklab must be a numpy array"):
        _check_valid_lab([0.0, 0.5, 1.0])


def test_invalid_lab_wrong_shape():
    """Oklab arrays with wrong shape should raise ValueError."""
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_lab(np.array([0.0, 0.5]))
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_lab(np.array([0.0, 0.5, 1.0, 0.5]))
    with pytest.raises(ValueError, match="numpy array length 3"):
        _check_valid_lab(np.array([[0.0, 0.5, 1.0]]))


def test_invalid_lab_L_out_of_range():
    """Oklab L values outside [0.0, 1.0] should raise ValueError."""
    with pytest.raises(ValueError, match="Oklab L value must be in"):
        _check_valid_lab(np.array([-0.1, 0.5, 1.0]))
    with pytest.raises(ValueError, match="Oklab L value must be in"):
        _check_valid_lab(np.array([1.1, 0.5, 1.0]))


def test_invalid_lab_non_numeric():
    """Oklab arrays with non-numeric values should raise ValueError."""
    with pytest.raises(ValueError, match="Oklab must have a numeric dtype"):
        _check_valid_lab(np.array([0.0, "0.5", 1.0]))
    with pytest.raises(ValueError, match="Oklab must have a numeric dtype"):
        _check_valid_lab(np.array([0.0, None, 1.0]))