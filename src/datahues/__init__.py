from .ramp import generate_hex_list, generate_cmap
from importlib.metadata import version

__version__ = version("datahues")
__all__ = ["generate_hex_list", "generate_cmap"]
