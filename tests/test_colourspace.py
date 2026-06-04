"""Tests for colourspace module."""
import numpy as np
import pytest
from datahues.colourspace import (
    _hex_to_oklab,
    _hex_to_srgb,
    _oklab_to_hex,
    _srgb_to_hex,
)

# fixtures below obtained using colour-science package for indep. testing
HEXES = ["#000000", "#ffffff", "#ff0000", "#00ff00", "#0000ff", '#969a9d', '#faea2c']
SRGBS = [
    np.array([0., 0., 0.]),
    np.array([1., 1., 1.]),
    np.array([1., 0., 0.]),
    np.array([0., 1., 0.]),
    np.array([0., 0., 1.]),
    np.array([0.58823529, 0.60392157, 0.61568627]),
    np.array([0.98039216, 0.91764706, 0.17254902]),
]
OKLABS = [
    np.array([0., 0., 0.]),
    np.array([1., 2.28547958e-06, -1.13652666e-04]),
    np.array([0.6279259, 0.2248876, 0.12580493]),
    np.array([0.86645187, -0.23392144, 0.17942177]),
    np.array([0.45203295, -0.03235164, -0.31162054]),
    np.array([0.68387042, -0.00321004, -0.00561177]),
    np.array([0.92142014, -0.04562476, 0.18034768]),
]


@pytest.mark.parametrize("hex, srgb", zip(HEXES, SRGBS))
def test_hex_to_srgb_conversions(hex, srgb):
    """Test colour conversion hex->sRGB."""
    np.testing.assert_allclose(_hex_to_srgb(hex), srgb)


@pytest.mark.parametrize("hex, srgb", zip(HEXES, SRGBS))
def test_srgb_to_hex_conversions(hex, srgb):
    """Test colour conversion sRGB->hex."""
    assert _srgb_to_hex(srgb).upper() == hex.upper()


@pytest.mark.parametrize("hex, oklab", zip(HEXES, OKLABS))
def test_hex_to_oklab_conversions(hex, oklab):
    """Test colour conversion hex->oklab."""
    np.testing.assert_allclose(_hex_to_oklab(hex), oklab, atol=1e-3)


@pytest.mark.parametrize("hex, oklab", zip(HEXES, OKLABS))
def test_oklab_to_hex_conversions(hex, oklab):
    """Test colour conversion oklab->hex."""
    hex2 = _oklab_to_hex(oklab)
    assert hex2.upper() == hex.upper()
