import unittest

import numpy as np
import pandas as pd
import xarray as xr
from o3skim import operations


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


class TestsLonMean(unittest.TestCase):

    def setUp(self) -> None:
        self.ds = operations.lon_mean(dataset)

    def test_keep_attrs(self):
        self.assertEqual(self.ds.attrs, dataset.attrs)
        for var in ['tco3_zm', 'vmro3_zm']:
            self.assertEqual(self.ds[var].attrs, dataset[var].attrs)

    def test_correct_coords(self):
        self.assertIn('time', self.ds.coords)
        self.assertIn('lat', self.ds.coords)
        self.assertNotIn('lon', self.ds.coords)
        self.assertIn('plev', self.ds.coords)


class TestsLatMean(unittest.TestCase):

    def setUp(self) -> None:
        self.ds = operations.lat_mean(dataset)

    def test_keep_attrs(self):
        self.assertEqual(self.ds.attrs, dataset.attrs)
        for var in ['tco3_zm', 'vmro3_zm']:
            self.assertEqual(self.ds[var].attrs, dataset[var].attrs)

    def test_correct_coords(self):
        self.assertIn('time', self.ds.coords)
        self.assertNotIn('lat', self.ds.coords)
        self.assertIn('lon', self.ds.coords)
        self.assertIn('plev', self.ds.coords)


class TestsRun(unittest.TestCase):

    def test_lon_mean(self):
        self.ds = operations.run('lon_mean', dataset)
        TestsLonMean.test_keep_attrs(self)
        TestsLonMean.test_correct_coords(self)

    def test_lat_mean(self):
        self.ds = operations.run('lat_mean', dataset)
        TestsLatMean.test_keep_attrs(self)
        TestsLatMean.test_correct_coords(self)
