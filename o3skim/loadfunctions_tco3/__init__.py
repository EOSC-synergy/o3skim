"""Module in charge of collecting source data loading packages."""
from os.path import dirname, basename, isdir, join
import glob
import importlib


__package_pathname = join(dirname(__file__), "*")
__directories = [f for f in glob.glob(__package_pathname) if isdir(f)]
__subpackages = [f for f in __directories if not f.endswith("__pycache__")]
__all__ = [basename(f) for f in __subpackages]


for module in __all__:
    importlib.import_module(f".{module}", __package__)
