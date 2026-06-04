import numpy as np
from .utils import (
    _check_valid_hex, _check_valid_rgb, _check_valid_xyz, _check_valid_lab
)

###############################################################################
# CONVERSION MATRICES
# (assume D65 white point)
###############################################################################

MATRIX_SRGB_TO_XYZ = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
])
MATRIX_XYZ_TO_SRGB = np.linalg.inv(MATRIX_SRGB_TO_XYZ)
MATRIX_XYZ_TO_LMS = np.array([
    [0.8189330101,  0.3618667424, -0.1288597137],
    [0.0329845436,  0.9293118715,  0.0361456387],
    [0.0482003018,  0.2643662691,  0.6338517070],
])
MATRIX_LMS_TO_XYZ = np.linalg.inv(MATRIX_XYZ_TO_LMS)
MATRIX_LMS_TO_LAB = np.array([
    [0.2104542553,  0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050,  0.4505937099],
    [0.0259040371,  0.7827717662, -0.8086757660],
])
MATRIX_LAB_TO_LMS = np.linalg.inv(MATRIX_LMS_TO_LAB)


###############################################################################
# INDIVIDUAL CONVERSIONS: hex -> sRGB -> linear RGB -> XYZ -> Oklab
###############################################################################

def _hex_to_srgb(hex: str) -> np.ndarray:
    """Convert hex colour code '#RRGGBB' to sRGB tuple in [0.0, 1.0]."""
    _check_valid_hex(hex)
    r = int(hex[1:3], 16) / 255.0
    g = int(hex[3:5], 16) / 255.0
    b = int(hex[5:7], 16) / 255.0
    rgb = np.array([r, g, b], dtype=float)
    return rgb


def _srgb_to_lrgb(srgb: np.ndarray) -> np.ndarray:
    """Convert sRGB to linear RGB (inverse companding / gamma removal)."""
    _check_valid_rgb(srgb)
    lrgb = np.where(
        srgb <= 0.04045,
        srgb / 12.92,
        ((srgb + 0.055) / 1.055) ** 2.4
    )
    lrgb = np.clip(lrgb, 0.0, 1.0)
    return lrgb


def _lrgb_to_xyz(lrgb: np.ndarray) -> np.ndarray:
    """Convert linear RGB to CIE XYZ (D65 illuminant)."""
    _check_valid_rgb(lrgb)
    xyz = lrgb @ MATRIX_SRGB_TO_XYZ.T
    xyz = np.clip(xyz, 0.0, None)
    return xyz


def _xyz_to_oklab(xyz: np.ndarray) -> np.ndarray:
    """Convert CIE XYZ (D65 illuminant) to Oklab."""
    _check_valid_xyz(xyz)
    lms = xyz @ MATRIX_XYZ_TO_LMS.T
    lab = np.cbrt(lms) @ MATRIX_LMS_TO_LAB.T
    return lab


###############################################################################
# INDIVIDUAL CONVERSIONS: Oklab -> XYZ -> linear RGB -> sRGB -> hex
###############################################################################


def _oklab_to_xyz(lab: np.ndarray) -> np.ndarray:
    """Convert Oklab to CIE XYZ (D65 illuminant)."""
    _check_valid_lab(lab)
    lms_cbrt = lab @ MATRIX_LAB_TO_LMS.T
    xyz = lms_cbrt ** 3 @ MATRIX_LMS_TO_XYZ.T
    xyz = np.clip(xyz, 0.0, None)
    return xyz


def _xyz_to_lrgb(xyz: np.ndarray) -> np.ndarray:
    """Convert CIE XYZ (D65 illuminant) to linear RGB."""
    _check_valid_xyz(xyz)
    lrgb = xyz @ MATRIX_XYZ_TO_SRGB.T
    lrgb = np.clip(lrgb, 0.0, 1.0)
    return lrgb


def _lrgb_to_srgb(c: np.ndarray) -> np.ndarray:
    """Convert linear RGB to sRGB (companding / gamma encoding)."""
    _check_valid_rgb(c)
    srgb = np.where(c <= 0.0031308, c * 12.92, 1.055 * c**(1.0 / 2.4) - 0.055)
    srgb = np.clip(srgb, 0.0, 1.0)
    return srgb


def _srgb_to_hex(srgb: np.ndarray) -> str:
    """Convert sRGB array in [0.0, 1.0] to hex colour code '#RRGGBB'."""
    _check_valid_rgb(srgb)
    r, g, b = (int(round(c * 255)) for c in srgb)
    return f"#{r:02X}{g:02X}{b:02X}"


###############################################################################
# FULL CASCADES: hex <-> Oklab
###############################################################################


def _hex_to_oklab(hex: str) -> np.ndarray:
    """Convert hex colour code to Oklab."""
    _check_valid_hex(hex)
    srgb = _hex_to_srgb(hex)
    lrgb = _srgb_to_lrgb(srgb)
    xyz = _lrgb_to_xyz(lrgb)
    lab = _xyz_to_oklab(xyz)
    return lab


def _oklab_to_hex(lab: np.ndarray) -> str:
    """Convert Oklab values to hex colour code."""
    _check_valid_lab(lab)
    xyz = _oklab_to_xyz(lab)
    lrgb = _xyz_to_lrgb(xyz)
    srgb = _lrgb_to_srgb(lrgb)
    hex = _srgb_to_hex(srgb)
    return hex
