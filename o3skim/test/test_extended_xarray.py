import unittest

import numpy as np
import pandas as pd
import xarray as xr
from o3skim import extended_xarray


longitude = [-180, 0, 180]
latitude = [-90, 0, 90]
pressure_level = [1, 10, 100, 1000]
time = pd.date_range("2000-01-01", periods=25, freq='A')

tco3_datarray = xr.DataArray(
    data=np.random.rand(3, 3, 25),
    dims=["lon", "lat", "time"],
    coords=dict(
        lon=longitude,
        lat=latitude,
        time=time),
    attrs=dict(description="Test tco3 xarray"))

vmro3_datarray = xr.DataArray(
    data=np.random.rand(3, 3, 4, 25),
    dims=["lon", "lat", "plev", "time"],
    coords=dict(
        lon=longitude,
        lat=latitude,
        plev=pressure_level,
        time=time),
    attrs=dict(description="Test vmro3 xarray"))

dataset = xr.Dataset(
    data_vars=dict(
        tco3_zm=tco3_datarray,
        vmro3_zm=vmro3_datarray),
    attrs=dict(description="Test dataset"))


class TestsTCO3Accessor(unittest.TestCase):

    def setUp(self) -> None:
        self.accessor = dataset.tco3

    def test_property_dataset(self):
        ds = self.accessor.dataset
        xr.testing.assert_equal(ds['tco3_zm'], tco3_datarray)
        self.assertEqual(ds['tco3_zm'].attrs, tco3_datarray.attrs)
        self.assertEqual(ds.attrs, dataset.attrs)
        self.assertIn('time', ds.coords)
        self.assertIn('lat', ds.coords)
        self.assertIn('lon', ds.coords)
        self.assertNotIn('plev', ds.coords)


class TestsVMRO3Accessor(unittest.TestCase):

    def setUp(self) -> None:
        self.accessor = dataset.vmro3

    def test_property_dataset(self):
        ds = self.accessor.dataset
        xr.testing.assert_equal(ds['vmro3_zm'], vmro3_datarray)
        self.assertEqual(ds['vmro3_zm'].attrs, vmro3_datarray.attrs)
        self.assertEqual(ds.attrs, dataset.attrs)
        self.assertIn('time', ds.coords)
        self.assertIn('lat', ds.coords)
        self.assertIn('lon', ds.coords)
        self.assertIn('plev', ds.coords)


class TestsO3Accessor(unittest.TestCase):

    def test_item_tco3(self):
        self.accessor = dataset.o3['tco3_zm']
        TestsTCO3Accessor.test_property_dataset(self)

    def test_item_vmro3(self):
        self.accessor = dataset.o3['vmro3_zm']
        TestsVMRO3Accessor.test_property_dataset(self)
