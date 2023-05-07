from ._version import __version__
from .modelrouter import (
    ModelRouter,
    model_to_pydantic
)

version = __version__

__all__ = [
    "ModelRouter",
    "model_to_pydantic",
    "version"
]
