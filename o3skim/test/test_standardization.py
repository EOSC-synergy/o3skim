import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import standardization


tco3_nonstd = xr.DataArray(
    data=np.mgrid[3:1:3j, 3:1:3j, 1:1:1j, 3:1:3j][0],
    dims=["long", "latd", "high", "time"],
    coords=dict(
        long=[180, 0, -180],
        latd=[90, 0, -90],
        high=[1],
        time=pd.date_range("2000-01-03", periods=3, freq='-1d')),
    attrs=dict(description="Non standardized DataArray"))

tco3_standard = xr.DataArray(
    data=np.mgrid[1:3:3j, 1:3:3j, 1:3:3j][0],
    dims=["lon", "lat", "time"],
    coords=dict(
        time=pd.date_range("2000-01-01", periods=3, freq='1d'),
        lat=[-90, 0, 90],
        lon=[-180, 0, 180]),
    attrs=dict(description="Standardized DataArray"))


class TestsTCO3(unittest.TestCase):

    def test_standardize(self):
        coords = {'lon': 'long', 'lat': 'latd', 'time': 'time'}
        standardized_tco3 = standardization.tco3(
            array=tco3_nonstd,
            coord=coords)
        xr.testing.assert_equal(tco3_standard, standardized_tco3)


vmro3_nonstd = xr.DataArray(
    data=np.mgrid[3:1:3j, 3:1:3j, 4:1:4j, 3:1:3j][0],
    dims=["lo", "la", "lv", "t"],
    coords=dict(
        lo=[180, 0, -180],
        la=[90, 0, -90],
        lv=[1000, 100, 10, 1],
        t=pd.date_range("2000-01-03", periods=3, freq='-1d')),
    attrs=dict(description="Non standardized DataArray"))

vmro3_standard = xr.DataArray(
    data=np.mgrid[1:3:3j, 1:3:3j, 1:4:4j, 1:3:3j][0],
    dims=["lon", "lat", "plev", "time"],
    coords=dict(
        time=pd.date_range("2000-01-01", periods=3, freq='1d'),
        plev=[1, 10, 100, 1000],
        lat=[-90, 0, 90],
        lon=[-180, 0, 180]),
    attrs=dict(description="Standardized DataArray"))


class TestsVMRO3(unittest.TestCase):

    def test_standardize(self):
        coords = {'lon': 'lo', 'lat': 'la', 'plev': 'lv', 'time': 't'}
        standardized_vmro3 = standardization.vmro3(
            array=vmro3_nonstd,
            coord=coords)
        xr.testing.assert_equal(vmro3_standard, standardized_vmro3)
