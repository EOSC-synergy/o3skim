"""Module in charge of dataset standardization when loading models."""

import logging
import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import utils

logger = logging.getLogger('o3skim.standardization')


@utils.return_on_failure("Error when loading '{0}'".format('tco3_zm'),
                         default=xr.Dataset())
def standardize_tco3(dataset, variable, coordinates):
    """Standardizes a tco3 dataset"""
    array = dataset[variable]
    array.name = 'tco3_zm'
    array = squeeze(array)
    array = rename_coords_tco3(array, **coordinates)
    array = sort(array)
    return array.to_dataset()


def rename_coords_tco3(array, time, lat, lon):
    """Renames a tco3 array variable and coordinates"""
    logger.debug("Renaming '{0}' coordinates".format('tco3_zm'))
    return array.rename({time: 'time', lat: 'lat', lon: 'lon'})


@utils.return_on_failure("Error when loading '{0}'".format('vmro3_zm'),
                         default=xr.Dataset())
def standardize_vmro3(dataset, variable, coordinates):
    """Standardizes a vmro3 dataset"""
    array = dataset[variable]
    array.name = 'vmro3_zm'
    array = squeeze(array)
    array = rename_coords_vmro3(array, **coordinates)
    array = sort(array)
    return array.to_dataset()


def rename_coords_vmro3(array, time, plev, lat, lon):
    """Renames a vmro3 array variable and coordinates"""
    logger.debug("Renaming '{0}' coordinates".format('vmro3_zm'))
    return array.rename({time: 'time', plev: 'plev', lat: 'lat', lon: 'lon'})


def squeeze(array):
    """Squeezes the 1-size dimensions on an array"""
    logger.debug("Squeezing coordinates in dataset")
    return array.squeeze(drop=True)


def sort(array):
    """Sorts an array by coordinates"""
    logger.debug("Sorting coordinates in dataset")
    return array.sortby(list(array.coords))


class TestsTCO3(unittest.TestCase):

    data_s = np.mgrid[1:3:3j, 1:3:3j, 1:3:3j][0]
    data_r = np.mgrid[3:1:3j, 3:1:3j, 1:1:1j, 3:1:3j][0]
    varname = "tco3"
    coords = {'lon': 'long', 'lat': 'latd', 'time': 'time'}

    @staticmethod
    def non_standard_ds():
        return xr.Dataset(
            data_vars=dict(
                tco3=(["long", "latd", "high", "time"], TestsTCO3.data_r)
            ),
            coords=dict(
                long=[180, 0, -180],
                latd=[90, 0, -90],
                high=[1],
                time=pd.date_range("2000-01-03", periods=3, freq='-1d')
            ),
            attrs=dict(description="Non standardized dataset")
        )

    @staticmethod
    def standard_ds():
        return xr.Dataset(
            data_vars=dict(
                tco3_zm=(["lon", "lat", "time"], TestsTCO3.data_s)
            ),
            coords=dict(
                time=pd.date_range("2000-01-01", periods=3, freq='1d'),
                lat=[-90, 0, 90],
                lon=[-180, 0, 180]
            ),
            attrs=dict(description="Standardized dataset")
        )

    def test_standardize(self):
        standardized_tco3 = standardize_tco3(
            dataset=TestsTCO3.non_standard_ds(),
            variable=TestsTCO3.varname,
            coordinates=TestsTCO3.coords)
        xr.testing.assert_equal(TestsTCO3.standard_ds(), standardized_tco3)

    def test_fail_returns_empty_dataset(self):
        empty_dataset = standardize_tco3(
            dataset=TestsTCO3.non_standard_ds(),
            variable="badVariable",
            coordinates=TestsTCO3.coords)
        xr.testing.assert_equal(xr.Dataset(), empty_dataset)


class TestsVMRO3(unittest.TestCase):

    data_s = np.mgrid[1:3:3j, 1:3:3j, 1:4:4j, 1:3:3j][0]
    data_r = np.mgrid[3:1:3j, 3:1:3j, 4:1:4j, 3:1:3j][0]
    varname = "vmro3"
    coords = {'lon': 'longit', 'lat': 'latitu',
              'plev': 'level', 'time': 't'}

    @staticmethod
    def non_standard_ds():
        return xr.Dataset(
            data_vars=dict(
                vmro3=(["longit", "latitu", "level", "t"], TestsVMRO3.data_r)
            ),
            coords=dict(
                longit=[180, 0, -180],
                latitu=[90, 0, -90],
                level=[1000, 100, 10, 1],
                t=pd.date_range("2000-01-03", periods=3, freq='-1d')
            ),
            attrs=dict(description="Non standardized dataset")
        )

    @staticmethod
    def standard_ds():
        return xr.Dataset(
            data_vars=dict(
                vmro3_zm=(["lon", "lat", "plev", "time"], TestsVMRO3.data_s)
            ),
            coords=dict(
                time=pd.date_range("2000-01-01", periods=3, freq='1d'),
                plev=[1, 10, 100, 1000],
                lat=[-90, 0, 90],
                lon=[-180, 0, 180]
            ),
            attrs=dict(description="Standardized dataset")
        )

    def test_standardize(self):
        standardized_vmro3 = standardize_vmro3(
            dataset=TestsVMRO3.non_standard_ds(),
            variable=TestsVMRO3.varname,
            coordinates=TestsVMRO3.coords)
        xr.testing.assert_equal(TestsVMRO3.standard_ds(), standardized_vmro3)

    def test_fail_returns_empty_dataset(self):
        empty_dataset = standardize_vmro3(
            dataset=TestsVMRO3.non_standard_ds(),
            variable="badVariable",
            coordinates=TestsVMRO3.coords)
        xr.testing.assert_equal(xr.Dataset(), empty_dataset)
