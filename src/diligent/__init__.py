"""Diligent module."""

from .cli import cli

__all__ = ["cli"]


from . import _version

__version__ = _version.get_versions()['version']
