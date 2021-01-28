import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import standardization

standardize_tco3 = standardization.standardize_tco3
standardize_vmro3 = standardization.standardize_vmro3


tco3_data_s = np.mgrid[1:3:3j, 1:3:3j, 1:3:3j][0]
tco3_data_r = np.mgrid[3:1:3j, 3:1:3j, 1:1:1j, 3:1:3j][0]
tco3_varname = "tco3"
tco3_coords = {'lon': 'long', 'lat': 'latd', 'time': 'time'}

tco3_nonstd = xr.Dataset(
    data_vars=dict(
        tco3=(["long", "latd", "high", "time"], tco3_data_r)
    ),
    coords=dict(
        long=[180, 0, -180],
        latd=[90, 0, -90],
        high=[1],
        time=pd.date_range("2000-01-03", periods=3, freq='-1d')
    ),
    attrs=dict(description="Non standardized dataset")
)

tco3_standard = xr.Dataset(
    data_vars=dict(
        tco3_zm=(["lon", "lat", "time"], tco3_data_s)
    ),
    coords=dict(
        time=pd.date_range("2000-01-01", periods=3, freq='1d'),
        lat=[-90, 0, 90],
        lon=[-180, 0, 180]
    ),
    attrs=dict(description="Standardized dataset")
)


class TestsTCO3(unittest.TestCase):

    def test_standardize(self):
        standardized_tco3 = standardize_tco3(
            dataset=tco3_nonstd,
            variable=tco3_varname,
            coordinates=tco3_coords)
        xr.testing.assert_equal(tco3_standard, standardized_tco3)

    def test_fail_returns_empty_dataset(self):
        empty_dataset = standardize_tco3(
            dataset=tco3_nonstd,
            variable="badVariable",
            coordinates=tco3_coords)
        xr.testing.assert_equal(xr.Dataset(), empty_dataset)


vmro3_data_s = np.mgrid[1:3:3j, 1:3:3j, 1:4:4j, 1:3:3j][0]
vmro3_data_r = np.mgrid[3:1:3j, 3:1:3j, 4:1:4j, 3:1:3j][0]
vmro3_varname = "vmro3"
vmro3_coords = {'lon': 'longit', 'lat': 'latitu',
                'plev': 'level', 'time': 't'}

vmro3_nonstd = xr.Dataset(
    data_vars=dict(
        vmro3=(["longit", "latitu", "level", "t"], vmro3_data_r)
    ),
    coords=dict(
        longit=[180, 0, -180],
        latitu=[90, 0, -90],
        level=[1000, 100, 10, 1],
        t=pd.date_range("2000-01-03", periods=3, freq='-1d')
    ),
    attrs=dict(description="Non standardized dataset")
)

vmro3_standard = xr.Dataset(
    data_vars=dict(
        vmro3_zm=(["lon", "lat", "plev", "time"], vmro3_data_s)
    ),
    coords=dict(
        time=pd.date_range("2000-01-01", periods=3, freq='1d'),
        plev=[1, 10, 100, 1000],
        lat=[-90, 0, 90],
        lon=[-180, 0, 180]
    ),
    attrs=dict(description="Standardized dataset")
)


class TestsVMRO3(unittest.TestCase):

    def test_standardize(self):
        standardized_vmro3 = standardize_vmro3(
            dataset=vmro3_nonstd,
            variable=vmro3_varname,
            coordinates=vmro3_coords)
        xr.testing.assert_equal(vmro3_standard, standardized_vmro3)

    def test_fail_returns_empty_dataset(self):
        empty_dataset = standardize_vmro3(
            dataset=vmro3_nonstd,
            variable="badVariable",
            coordinates=vmro3_coords)
        xr.testing.assert_equal(xr.Dataset(), empty_dataset)
