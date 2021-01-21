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


@xr.register_dataset_accessor("model")
class ModelAccessor:
    def __init__(self, xarray_obj):
        self._model = xarray_obj

    @property
    def tco3(self):
        """Return the total ozone column of this dataset."""
        return self._model["tco3_zm"]

    @property
    def vmro3(self):
        """Return the ozone volume mixing ratio of this dataset."""
        return self._model["vmro3_zm"]

    def groupby(self, delta='year'):
        """ """
        pass #TODO

    def to_netcdf(self, delta=None):
        """ """
        pass #TODO


class Tests(unittest.TestCase):

    tco3 = np.random.rand(3, 3, 3)
    vmro3 = np.random.rand(3, 3, 4, 3)
    longitude = [-180, 0, 180]
    latitude = [-90, 0, 90]
    pressure_level = [1, 10, 100, 1000]
    time = pd.date_range("2000-01-01", periods=3)

    @staticmethod
    def tco3_datarray():
        return xr.DataArray(
            data=Tests.tco3,
            dims=["lon", "lat", "time"],
            coords=dict(
                lon=Tests.longitude,
                lat=Tests.latitude,
                time=Tests.time
            ),
            attrs=dict(description="Test tco3 datarray")
        )
    
    @staticmethod
    def vmro3_datarray():
        return xr.DataArray(
            data=Tests.vmro3,
            dims=["lon", "lat", "plev", "time"],
            coords=dict(
                lon=Tests.longitude,
                lat=Tests.latitude,
                plev=Tests.pressure_level,
                time=Tests.time
            ),
            attrs=dict(description="Test vmro3 datarray")
        )

    def setUp(self):
        self.ds = xr.Dataset(
            data_vars=dict(
                tco3_zm=self.tco3_datarray(),
                vmro3_zm=self.vmro3_datarray()
            ),
            coords=dict(
                lon=Tests.longitude,
                lat=Tests.latitude,
                plev=Tests.pressure_level,
                time=Tests.time
            ),
            attrs=dict(description="Test dataset")
        )

    def test_tco3_property(self):
        xr.testing.assert_equal(self.ds.model.tco3, Tests.tco3_datarray())

    def test_vmro3_property(self):
        xr.testing.assert_equal(self.ds.model.vmro3, Tests.vmro3_datarray())
