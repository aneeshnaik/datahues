"""Tests for ramp module."""
from matplotlib.colors import LinearSegmentedColormap
import pytest
from datahues.ramp import generate_cmap, generate_hex_list


###############################################################################
# Tests for generate_hex_list
###############################################################################


@pytest.mark.parametrize(
    "badhex", [123, True, None, "FF0000", "#FF00", "#FF00000", "#GGGGGG"]
)
def test_generate_hex_list_invalid_start_hex(badhex):
    """Bad input start hex should raise ValueError."""
    with pytest.raises(ValueError):
        generate_hex_list(badhex, "#0000FF")


@pytest.mark.parametrize(
    "badhex", [123, True, None, "FF0000", "#FF00", "#FF00000", "#GGGGGG"]
)
def test_generate_hex_list_invalid_end_hex(badhex):
    """Bad input end hex should raise ValueError."""
    with pytest.raises(ValueError):
        generate_hex_list("#0000FF", badhex)


def test_generate_hex_list_returns_list_of_strings():
    """Should return a list of hex strings."""
    result = generate_hex_list("#FF0000", "#0000FF", n_stops=5)
    assert isinstance(result, list)
    assert all(isinstance(h, str) for h in result)


def test_generate_hex_list_correct_number_of_stops():
    """Should return the correct number of colours."""
    result = generate_hex_list("#FF0000", "#0000FF", n_stops=10)
    assert len(result) == 10


def test_generate_hex_list_starts_and_ends_correctly():
    """First and last colours should match input exactly."""
    start = "#FF0000"
    end = "#0000FF"
    result = generate_hex_list(start, end, n_stops=5)
    assert result[0] == start.upper()
    assert result[-1] == end.upper()


def test_generate_hex_list_default_n_stops():
    """Default n_stops should be 512."""
    result = generate_hex_list("#FF0000", "#0000FF")
    assert len(result) == 512


###############################################################################
# Tests for generate_cmap
###############################################################################


def test_generate_cmap_low_n_stops_warning():
    """Should warn if n_stops < 128."""
    with pytest.warns(UserWarning, match="banding"):
        generate_cmap("#FF0000", "#0000FF", n_stops=50)


def test_generate_cmap_returns_linear_segmented_colormap():
    """Should return a LinearSegmentedColormap object."""
    result = generate_cmap("#FF0000", "#0000FF")
    assert isinstance(result, LinearSegmentedColormap)


def test_generate_cmap_colormap_has_correct_name():
    """Colormap should have the specified name."""
    result = generate_cmap("#FF0000", "#0000FF", name="test_cmap")
    assert result.name == "test_cmap"


def test_generate_cmap_colormap_default_name():
    """Colormap should use default name if not specified."""
    result = generate_cmap("#FF0000", "#0000FF")
    assert result.name == "interp_ramp"
