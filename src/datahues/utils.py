"""Utility functions for datahues."""
import numpy as np


def _check_valid_hex(hex: str) -> None:
    """
    Validate that input string is a valid hex colour code.

    Checks that the input is a string in the format '#RRGGBB' with valid
    hexadecimal digits. Raises error if not.

    Parameters
    ----------
    hex : str
        Hex colour code to validate.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If hex is not a string, doesn't start with '#', isn't exactly 7
        characters long, or contains invalid hexadecimal digits.
    """
    if not isinstance(hex, str):
        raise ValueError("Hex must be a string.")
    if not hex.startswith('#') or len(hex) != 7:
        raise ValueError("Hex must start with '#' and be 7 characters long.")
    try:
        int(hex[1:], 16)
    except ValueError:
        raise ValueError("Hex must contain valid hexadecimal digits.")


def _check_valid_rgb(rgb: np.ndarray) -> None:
    """
    Validate that input array is a valid sRGB or linear RGB colour.

    Checks that the input is a numpy array of 3 numeric values in the range
    [0.0, 1.0]. Raises error if not.

    Parameters
    ----------
    rgb : array-like
        RGB colour to validate.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If rgb is not numpy array of 3 floats or any value outside [0.0, 1.0].
    """
    if not isinstance(rgb, np.ndarray):
        raise ValueError("RGB must be a numpy array.")
    if rgb.shape != (3,):
        raise ValueError("RGB must be a numpy array length 3.")
    if not np.issubdtype(rgb.dtype, np.number):
        raise ValueError("RGB must have a numeric dtype.")
    if not np.all((rgb >= 0.0) & (rgb <= 1.0)):
        raise ValueError("RGB values must be in [0.0, 1.0].")


def _check_valid_xyz(xyz: np.ndarray) -> None:
    """
    Validate that input array is a valid XYZ colour.

    Checks that the input is a numpy array of 3 numeric values, where X, Y, Z
    are all non-negative. Raises error if not.

    Parameters
    ----------
    xyz : array-like
        XYZ colour to validate.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If xyz is not a numpy array of 3 floats or any value is negative.
    """
    if not isinstance(xyz, np.ndarray):
        raise ValueError("XYZ must be a numpy array.")
    if xyz.shape != (3,):
        raise ValueError("XYZ must be a numpy array length 3.")
    if not np.issubdtype(xyz.dtype, np.number):
        raise ValueError("XYZ must have a numeric dtype.")
    if np.any(xyz < 0.0):
        raise ValueError("XYZ values must be non-negative.")


def _check_valid_lab(lab: np.ndarray) -> None:
    """
    Validate that input array is a valid Oklab colour.

    Checks that the input is a numpy array of 3 numeric values, where L is in
    [0.0, 1.0]. Raises error if not.
    
    Note: a, b are typically in [-0.5, 0.5] but can be outside for very
    saturated colours. This is not checked here.

    Parameters
    ----------
    lab : array-like
        Oklab colour to validate.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If lab is not a numpy array of 3 floats or L is outside [0.0, 1.0].
    """
    if not isinstance(lab, np.ndarray):
        raise ValueError("Oklab must be a numpy array.")
    if lab.shape != (3,):
        raise ValueError("Oklab must be a numpy array length 3.")
    if not np.issubdtype(lab.dtype, np.number):
        raise ValueError("Oklab must have a numeric dtype.")
    if not (0.0 <= lab[0] <= 1.0):
        raise ValueError("Oklab L value must be in [0.0, 1.0].")
