"""Tests for colourspace module."""
import numpy as np
import pytest
from datahues.colourspace import (
    _hex_to_srgb,
)


def test_hex_to_srgb_conversions():
    """Test conversion of primary colors."""
    assert np.all(_hex_to_srgb("#000000") == np.array([0., 0., 0.]))


# TODO check full hex -> oklab conversion