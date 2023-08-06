try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

# replace the asterisk with named imports
from .napari_demo import napari_experimental_provide_function


__all__ = ["napari_experimental_provide_function"]
