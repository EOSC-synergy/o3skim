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


class Tests(unittest.TestCase):

    tco3 = np.random.rand(3, 3, 25)
    vmro3 = np.random.rand(3, 3, 4, 25)
    longitude = [-180, 0, 180]
    latitude = [-90, 0, 90]
    pressure_level = [1, 10, 100, 1000]
    time = pd.date_range("2000-01-01", periods=25, freq='A')

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
        expected = Tests.tco3_datarray().to_dataset(name="tco3_zm")
        xr.testing.assert_equal(self.ds.model.tco3, expected)

    def test_vmro3_property(self):
        expected = Tests.vmro3_datarray().to_dataset(name="vmro3_zm")
        xr.testing.assert_equal(self.ds.model.vmro3, expected)

    def test_metadata_property(self):
        metadata = self.ds.model.metadata
        self.assertEqual(metadata["description"], "Test dataset")
        self.assertEqual(metadata["tco3_zm"]
                         ["description"], "Test tco3 datarray")
        self.assertEqual(metadata["vmro3_zm"]
                         ["description"], "Test vmro3 datarray")

    def test_groupby_year(self):
        groups = self.ds.model.groupby_year()
        self.assertEqual(25, len(groups))
        for year, dataset in groups:
            self.assertIsInstance(year, np.int64)
            self.assertIsInstance(dataset, xr.Dataset)

    def test_groupby_decade(self):
        groups = self.ds.model.groupby_decade()
        self.assertEqual(3, len(groups))
        for decade, dataset in groups:
            self.assertIsInstance(decade, np.int64)
            self.assertIsInstance(dataset, xr.Dataset)

    def test_skimming(self):
        result = self.ds.model.skim()
        # Test general coordinates
        self.assertIn('time', result.coords)
        self.assertIn('lat', result.coords)
        self.assertIn('plev', result.coords)
        self.assertNotIn('lon', result.coords)
        # Test tco3 coordinates
        self.assertIn('time', result.model.tco3.coords)
        self.assertIn('lat', result.model.tco3.coords)
        self.assertNotIn('plev', result.model.tco3.coords)
        self.assertNotIn('lon', result.model.tco3.coords)
        # Test vmro3 coordinates
        self.assertIn('time', result.model.vmro3.coords)
        self.assertIn('lat', result.model.vmro3.coords)
        self.assertIn('plev', result.model.vmro3.coords)
        self.assertNotIn('lon', result.model.vmro3.coords)
