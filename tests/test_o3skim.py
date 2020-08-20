"""Unittest module template."""


import os
import unittest
import xarray as xr
import glob

from o3skim import sources, utils
# from pyfakefs.fake_filesystem_unittest import TestCase
from . import mockup_data


class TestO3SKIM_sources(unittest.TestCase):
    """Tests for `sources` package."""

    def setUp(self):
        """Loads and creates the test folders and files from test_sources.yaml"""
        self.config = sources.load("tests/test_sources.yaml")
        self.assertTrue(type(self.config) is dict)

        self.create_mock_datasets()
        self.backup_datasets()
        self.assert_with_backup()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def create_mock_datasets(self):
        """Creates mock data files according to the loaded configuration"""
        for source, collection in self.config.items():
            for model, variables in collection.items():
                for v, vinfo in variables.items():
                    path = "data/" + vinfo["dir"]
                    os.makedirs(path, exist_ok=True)
                    mockup_data.netcdf(path, **vinfo)

    def backup_datasets(self):
        """Loads the mock datasets into an internal variable"""
        self.ds_backup = {}
        for source, collection in self.config.items():
            self.ds_backup[source] = {}
            for model, variables in collection.items():
                self.ds_backup[source][model] = {}
                for v, vinfo in variables.items():
                    paths = "data/" + vinfo["dir"] + "/*.nc"
                    with xr.open_mfdataset(paths) as ds:
                        self.ds_backup[source][model][v] = ds

    def assert_with_backup(self):
        """Asserts the dataset in the backup is equal to the config load"""
        for source, collection in self.config.items():
            for model, variables in collection.items():
                for v, vinfo in variables.items():
                    paths = "data/" + vinfo["dir"] + "/*.nc"
                    with xr.open_mfdataset(paths) as ds:
                        xr.testing.assert_identical(
                            self.ds_backup[source][model][v], ds)

    def test_000_SourcesFromConfig(self):
        """Creates the different sources from the configuration file"""
        with utils.cd("data"):
            ds = {source: sources.Source(collection) for
                  source, collection in self.config.items()}

        # CCMI-1 tco3_zm asserts
        self.assertTrue('time' in ds['CCMI-1'].model['IPSL'].tco3_zm.coords)
        self.assertTrue('lon' in ds['CCMI-1'].model['IPSL'].tco3_zm.coords)
        self.assertTrue('lat' in ds['CCMI-1'].model['IPSL'].tco3_zm.coords)

        # CCMI-1 vrm_zm asserts
        self.assertTrue('time' in ds['CCMI-1'].model['IPSL'].vrm_zm.coords)
        self.assertTrue('plev' in ds['CCMI-1'].model['IPSL'].vrm_zm.coords)
        self.assertTrue('lon' in ds['CCMI-1'].model['IPSL'].vrm_zm.coords)
        self.assertTrue('lat' in ds['CCMI-1'].model['IPSL'].vrm_zm.coords)

        # Checks the original data has not been modified
        self.assert_with_backup()
