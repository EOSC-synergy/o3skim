"""
Main package with classes and utilities to handle ozone data skimming.

After the data are loaded and the instances created,
it is possible to use the internal methods to produce
the desired output.
"""

from o3skim import extended_xarray
from o3skim import source
from o3skim import standardization
from o3skim import utils

Source = source.Source
