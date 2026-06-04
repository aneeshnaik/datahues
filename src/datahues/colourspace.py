import numpy as np


# matrices for colour space conversions (assume D65 white point)
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


def _hex_to_rgb(hex: str) -> tuple[float, float, float]:
    """Convert hex colour code '#RRGGBB' to RGB tuple in [0.0, 1.0]."""
    r = int(hex[1:3], 16) / 255.0
    g = int(hex[3:5], 16) / 255.0
    b = int(hex[5:7], 16) / 255.0
    return (r, g, b)


def _rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    """Convert RGB tuple in [0.0, 1.0] to hex colour code '#RRGGBB'."""
    r, g, b = (int(c * 255) for c in rgb)
    return f"#{r:02X}{g:02X}{b:02X}"


def _srgb_to_linear(c: np.ndarray) -> np.ndarray:
    """Apply sRGB inverse companding (gamma removal) elementwise."""
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c: np.ndarray) -> np.ndarray:
    """Apply sRGB companding (gamma encoding) elementwise."""
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c**(1.0 / 2.4) - 0.055)


def _srgb_to_xyz(rgb: np.ndarray) -> np.ndarray:
    """Convert sRGB to CIE XYZ (D65 illuminant)."""
    rgb = np.asarray(rgb, dtype=float)
    if not np.all((rgb >= 0.0) & (rgb <= 1.0)):
        raise ValueError("RGB values must be in [0.0, 1.0].")
    return _srgb_to_linear(rgb) @ MATRIX_SRGB_TO_XYZ.T


def _xyz_to_srgb(xyz: np.ndarray) -> np.ndarray:
    """Convert CIE XYZ (D65 illuminant) to sRGB."""
    xyz = np.asarray(xyz, dtype=float)
    rgb_linear = xyz @ MATRIX_XYZ_TO_SRGB.T
    return np.clip(_linear_to_srgb(rgb_linear), 0.0, 1.0)


def _xyz_to_oklab(xyz: np.ndarray) -> np.ndarray:
    """Convert CIE XYZ (D65 illuminant) to Oklab."""
    xyz = np.asarray(xyz, dtype=float)
    lms = xyz @ MATRIX_XYZ_TO_LMS.T
    return np.cbrt(lms) @ MATRIX_LMS_TO_LAB.T


def _oklab_to_xyz(lab: np.ndarray) -> np.ndarray:
    """Convert Oklab to CIE XYZ (D65 illuminant)."""
    lab = np.asarray(lab, dtype=float)
    lms_cbrt = lab @ MATRIX_LAB_TO_LMS.T
    return lms_cbrt ** 3 @ MATRIX_LMS_TO_XYZ.T


def _hex_to_oklab(hex: str) -> np.ndarray:
    """Convert hex colour code to Oklab."""
    return _xyz_to_oklab(_srgb_to_xyz(_hex_to_rgb(hex)))


def _oklab_to_hex(lab: np.ndarray) -> str:
    """Convert Oklab values to hex colour code."""
    return _rgb_to_hex(_xyz_to_srgb(_oklab_to_xyz(lab)))
