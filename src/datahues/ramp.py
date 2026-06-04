import numpy as np
import warnings
from matplotlib.colors import LinearSegmentedColormap
from .utils import _check_valid_hex
from .colourspace import (
    _hex_to_oklab,
    _oklab_to_hex,
)


def generate_hex_list(
    start_hex: str, end_hex: str, n_stops: int = 512,
) -> list[str]:
    """
    Generate a list of hex colours forming a perceptually uniform ramp.

    Between user-specified start and end colours, creates straight line with
    user-specified number of stops in Oklab colour space, which is perceptually
    uniform. This ensures that colour transitions feel smooth and natural
    across the entire gradient. Returns colours as list of hex code strings.

    Note: It is assumed the user wants a discrete number (`n_stops`) of points,
    so no warning is given when `n_stops` is small (unlike in the
    `generate_cmap` function). However, if these hexes are being used to create
    a continuous colour ramp, it is recommended to use `n_stops`>=128.

    Parameters
    ----------
    start_hex : str
        Starting colour as hex code (e.g., '#FF0000').
    end_hex : str
        Ending colour as hex code (e.g., '#0000FF').
    n_stops : int, optional
        Number of colour stops in the ramp. Default is 512.

    Returns
    -------
    list[str]
        List of hex colour codes forming the gradient.

    Raises
    ------
    ValueError
        If start_hex or end_hex are not valid hex colour codes in format
        '#RRGGBB'.

    """
    # check that provided hexes are valid
    _check_valid_hex(start_hex)
    _check_valid_hex(end_hex)

    # convert hexes to Oklab space
    start_lab = _hex_to_oklab(start_hex)
    end_lab = _hex_to_oklab(end_hex)

    # generate n_stops evenly spaced values
    lab_ramp = np.linspace(start_lab, end_lab, n_stops)

    # convert back to hexes
    hex_ramp = [_oklab_to_hex(lab) for lab in lab_ramp]

    # reinsert original start and end hexes to ensure exact match
    hex_ramp[0] = start_hex.upper()
    hex_ramp[-1] = end_hex.upper()
    return hex_ramp


def generate_cmap(
    start_hex: str, end_hex: str, n_stops: int = 512, name: str = "interp_ramp"
) -> LinearSegmentedColormap:
    """
    Generate a Matplotlib colour map from start and end hex colours.

    Between user-specified start and end colours, creates straight line with
    user-specified number of stops in Oklab colour space, which is perceptually
    uniform. This ensures that colour transitions feel smooth and natural
    across the entire gradient. Returns colours as a LinearSegmentedColormap
    suitable for use with matplotlib visualisation functions

    Parameters
    ----------
    start_hex : str
        Starting colour as hex code (e.g., '#FF0000').
    end_hex : str
        Ending colour as hex code (e.g., '#0000FF').
    n_stops : int, optional
        Number of colour stops in the ramp. Default is 512.
    name : str, optional
        Name for the colormap. Default is 'interp_ramp'.

    Returns
    -------
    LinearSegmentedColormap
        Matplotlib colormap ready for use in plotting functions.

    Raises
    ------
    ValueError
        If start_hex or end_hex are not valid hex colour codes in format
        '#RRGGBB'.

    Warnings
    --------
    UserWarning
        If n_stops < 128, which may produce visible banding in the colormap.

    Examples
    --------
    >>> cmap = generate_cmap('#FF0000', '#0000FF', n_stops=256)
    >>> # Use in matplotlib
    >>> import matplotlib.pyplot as plt
    >>> plt.imshow(data, cmap=cmap)
    """
    # warn if n_stops is too low for smooth interpolation
    if n_stops < 128:
        warnings.warn(
            "n_stops < 128 may produce visible banding in the colour ramp. "
            "Consider using a larger n_stops for smoother gradients.",
        )

    hex_list = generate_hex_list(start_hex, end_hex, n_stops)
    return LinearSegmentedColormap.from_list(name, hex_list)
