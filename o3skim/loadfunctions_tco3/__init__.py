"""Module in charge of collecting models data loading functions."""
from os.path import dirname, basename, isfile, join
import glob
import importlib


__package_pathname = join(dirname(__file__), "*.py")
__pyfiles = [f for f in glob.glob(__package_pathname) if isfile(f)]
__modules = [f for f in __pyfiles if not f.endswith("__init__.py")]
__all__ = [basename(f)[:-3] for f in __modules]


for module in __all__:
    importlib.import_module(f".{module}", __package__)
