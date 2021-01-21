"""Module in charge of dataset standardization when loading models."""

import logging
import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import utils

logger = logging.getLogger('o3skim.standardization')

# tco3 standardization
tco3_standard_name = 'tco3_zm'
tco3_standard_coordinates = [
    'time',
    'lat',
    'lon'
]

# vmro3 standardization
vmro3_standard_name = 'vmro3_zm'
vmro3_standard_coordinates = [
    'time',
    'plev',
    'lat',
    'lon'
]


def standardize(dataset, tco3_zm=None, vmro3_zm=None):
    pass  # TODO


def standardize_vmro3(dataset, variable, coordinates):
    """Standardizes a vmro3 dataset"""
    dataset = rename_vmro3(dataset, variable, coordinates)
    dataset = sort(dataset)
    return dataset


def rename_vmro3(dataset, variable, coordinates):
    """Renames a vmro3 dataset variable and coordinates"""
    logger.debug("Rename of '{0}' var and coords".format(vmro3_standard_name))
    return dataset.rename({
        **{variable: vmro3_standard_name},
        **{coordinates[x]: x for x in vmro3_standard_coordinates}
    })


def sort(dataset):
    """Sorts a dataset by coordinates"""
    logger.debug("Sorting coordinates in dataset")
    return dataset.sortby(list(dataset.coords))


def squeeze(dataset):
    """Squeezes the 1size dimensions on a dataset"""
    logger.debug("Squeezing coordinates in dataset")
    pass  # TODO


class TestsVMRO3(unittest.TestCase):

    data_s = np.mgrid[1:3:3j, 1:3:3j, 1:4:4j, 1:3:3j][0]
    data_r = np.mgrid[3:1:3j, 3:1:3j, 4:1:4j, 3:1:3j][0]

    varname = "vmro3"
    coords = {'lon': 'longit', 'lat': 'latitu',
              'plev': 'level', 'time': 'time'}

    @staticmethod
    def non_standard_ds():
        return xr.Dataset(
            data_vars=dict(
                vmro3=(["longit", "latitu", "level", "time"], TestsVMRO3.data_r)
            ),
            coords=dict(
                longit=[180, 0, -180],
                latitu=[90, 0, -90],
                level=[1000, 100, 10, 1],
                time=pd.date_range("2000-01-03", periods=3, freq='-1d')
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
