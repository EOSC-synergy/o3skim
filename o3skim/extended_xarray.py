"""
xarray extension module to provide model class and functions to handle
tco3 and vmro3 operations and data skimming.
"""
import logging
import os
import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import standardization

logger = logging.getLogger('extended_xr')
mean_coord = 'lon'


@xr.register_dataset_accessor("model")
class ModelAccessor:
    def __init__(self, xarray_obj):
        self._model = xarray_obj

    @property
    def tco3(self):
        """Return the total ozone column of this dataset."""
        if "tco3_zm" in list(self._model.var()):
            return self._model["tco3_zm"].to_dataset()
        else:
            return None

    @property
    def vmro3(self):
        """Return the ozone volume mixing ratio of this dataset."""
        if "vmro3_zm" in list(self._model.var()):
            return self._model["vmro3_zm"].to_dataset()
        else:
            return None

    @property
    def metadata(self):
        """Return the ozone volume mixing ratio of this dataset."""
        result = self._model.attrs
        for var in self._model.var():
            result = {**result, var: self._model[var].attrs}
        return result

    def groupby_year(self):
        """Returns a grouped dataset by year"""
        logger.debug("Performing group by year on model")
        def delta_map(x): return x.year
        years = self._model.indexes['time'].map(delta_map)
        return self._model.groupby(xr.DataArray(years))

    def groupby_decade(self):
        """Returns a grouped dataset by decade"""
        logger.debug("Performing group by decade on model")
        def delta_map(x): return x.year // 10 * 10
        years = self._model.indexes['time'].map(delta_map)
        return self._model.groupby(xr.DataArray(years))

    def skim(self):
        """Skims model producing reduced dataset"""
        logger.debug("Skimming model")
        return self._model.mean(mean_coord)

