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
from o3skim import standardization, utils

logger = logging.getLogger('extended_xr')
mean_coord = 'lon'


@xr.register_dataset_accessor("model")
class ModelAccessor:
    def __init__(self, xarray_obj):
        self._model = xarray_obj
        self._metadata = {}

    @property
    def tco3(self):
        """Return the total ozone column of this dataset."""
        if "tco3_zm" in list(self._model.var()):
            dataset = self._model["tco3_zm"].to_dataset()
            dataset.attrs = self._model.attrs
            return dataset
        else:
            return None

    @property
    def vmro3(self):
        """Return the ozone volume mixing ratio of this dataset."""
        if "vmro3_zm" in list(self._model.var()):
            dataset = self._model["vmro3_zm"].to_dataset()
            dataset.attrs = self._model.attrs
            return dataset
        else:
            return None

    @property
    def metadata(self):
        """Returns the metadata property"""
        return self._metadata

    def add_metadata(self, metadata):
        """Merges the input metadata with the model metadata"""
        utils.mergedicts(self._metadata, metadata)

    def set_metadata(self, metadata):
        """Sets the metadata to the input variable."""
        self._metadata = metadata

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
        skimmed = self._model.mean(mean_coord)
        skimmed.attrs = self._model.attrs
        for var in self._model:
            skimmed[var].attrs = self._model[var].attrs
        return skimmed
