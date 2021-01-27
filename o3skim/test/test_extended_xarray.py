import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import extended_xarray


tco3 = np.random.rand(3, 3, 25)
vmro3 = np.random.rand(3, 3, 4, 25)
longitude = [-180, 0, 180]
latitude = [-90, 0, 90]
pressure_level = [1, 10, 100, 1000]
time = pd.date_range("2000-01-01", periods=25, freq='A')

tco3_datarray = xr.DataArray(
    data=tco3,
    dims=["lon", "lat", "time"],
    coords=dict(
        lon=longitude,
        lat=latitude,
        time=time
    ),
    attrs=dict(description="Test tco3 xarray")
)

vmro3_datarray = xr.DataArray(
    data=vmro3,
    dims=["lon", "lat", "plev", "time"],
    coords=dict(
        lon=longitude,
        lat=latitude,
        plev=pressure_level,
        time=time
    ),
    attrs=dict(description="Test vmro3 xarray")
)

dataset = xr.Dataset(
    data_vars=dict(
        tco3_zm=tco3_datarray,
        vmro3_zm=vmro3_datarray
    ),
    coords=dict(
        lon=longitude,
        lat=latitude,
        plev=pressure_level,
        time=time
    ),
    attrs=dict(description="Test dataset")
)


class Tests(unittest.TestCase):

    def test_tco3_property(self):
        expected = tco3_datarray.to_dataset(name="tco3_zm")
        xr.testing.assert_equal(dataset.model.tco3, expected)

    def test_vmro3_property(self):
        expected = vmro3_datarray.to_dataset(name="vmro3_zm")
        xr.testing.assert_equal(dataset.model.vmro3, expected)

    def test_metadata_property(self):
        meta = dataset.model.metadata
        self.assertEqual(meta["description"], "Test dataset")
        self.assertEqual(meta["tco3_zm"]["description"], "Test tco3 xarray")
        self.assertEqual(meta["vmro3_zm"]["description"], "Test vmro3 xarray")

    def test_groupby_year(self):
        groups = dataset.model.groupby_year()
        self.assertEqual(25, len(groups))
        for year, ds in groups:
            self.assertIsInstance(year, np.int64)
            self.assertIsInstance(ds, xr.Dataset)

    def test_groupby_decade(self):
        groups = dataset.model.groupby_decade()
        self.assertEqual(3, len(groups))
        for decade, ds in groups:
            self.assertIsInstance(decade, np.int64)
            self.assertIsInstance(ds, xr.Dataset)

    def test_skimming_gen_coords(self):
        result = dataset.model.skim()
        self.assertIn('time', result.coords)
        self.assertIn('lat', result.coords)
        self.assertIn('plev', result.coords)
        self.assertNotIn('lon', result.coords)

    def test_skimming_tco3_coords(self):
        result = dataset.model.skim()
        self.assertIn('time', result.model.tco3.coords)
        self.assertIn('lat', result.model.tco3.coords)
        self.assertNotIn('plev', result.model.tco3.coords)
        self.assertNotIn('lon', result.model.tco3.coords)

    def test_skimming_vmro3_coords(self):
        result = dataset.model.skim()
        self.assertIn('time', result.model.vmro3.coords)
        self.assertIn('lat', result.model.vmro3.coords)
        self.assertIn('plev', result.model.vmro3.coords)
        self.assertNotIn('lon', result.model.vmro3.coords)
