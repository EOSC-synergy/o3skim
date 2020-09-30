"""Unittest module template."""


import os
import shutil
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
        self.config_base = utils.load("tests/sources_base.yaml")
        self.assertTrue(type(self.config_base) is dict)
        self.config_err = utils.load("tests/sources_err.yaml")
        self.assertTrue(type(self.config_err) is dict)

        self.create_mock_datasets()
        self.backup_datasets()
        self.assert_with_backup()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def create_mock_datasets(self):
        """Creates mock data files according to the loaded configuration"""
        for _, collection in self.config_base.items():
            for _, variables in collection.items():
                for _, vinfo in variables.items():
                    path = "data/" + vinfo["dir"]
                    os.makedirs(path, exist_ok=True)
                    mockup_data.netcdf(path, **vinfo)

    def clean_output(self):
        """Cleans output removing all folders at output"""
        with utils.cd("output"):
            directories = (d for d in os.listdir() if os.path.isdir(d))
            for directory in directories:
                shutil.rmtree(directory) 

    def backup_datasets(self):
        """Loads the mock datasets into an internal variable"""
        self.ds_backup = {}
        for source, collection in self.config_base.items():
            self.ds_backup[source] = {}
            for model, variables in collection.items():
                self.ds_backup[source][model] = {}
                for v, vinfo in variables.items():
                    paths = "data/" + vinfo["dir"] + "/*.nc"
                    with xr.open_mfdataset(paths) as ds:
                        self.ds_backup[source][model][v] = ds

    def assert_with_backup(self):
        """Asserts the dataset in the backup is equal to the config load"""
        for source, collection in self.config_base.items():
            for model, variables in collection.items():
                for v, vinfo in variables.items():
                    paths = "data/" + vinfo["dir"] + "/*.nc"
                    with xr.open_mfdataset(paths) as ds:
                        xr.testing.assert_identical(
                            self.ds_backup[source][model][v], ds)

    def test_001_SourcesFromConfig(self):
        """Creates the different sources from the configuration file"""
        with utils.cd("data"):
            ds = {name: sources.Source(name, collection) for
                  name, collection in self.config_base.items()}

        # CCMI-1 tco3_zm asserts
        self.assertTrue('time' in ds['CCMI-1']._models['IPSL']._tco3_zm.coords)
        self.assertTrue('lat' in ds['CCMI-1']._models['IPSL']._tco3_zm.coords)
        self.assertFalse('lon' in ds['CCMI-1']._models['IPSL']._tco3_zm.coords)

        # CCMI-1 vmro3_zm asserts
        self.assertTrue('time' in ds['CCMI-1']._models['IPSL']._vmro3_zm.coords)
        self.assertTrue('plev' in ds['CCMI-1']._models['IPSL']._vmro3_zm.coords)
        self.assertTrue('lat' in ds['CCMI-1']._models['IPSL']._vmro3_zm.coords)
        self.assertFalse('lon' in ds['CCMI-1']._models['IPSL']._vmro3_zm.coords)

        # Checks the original data has not been modified
        self.assert_with_backup()

    def test_002_OutputFromSources(self):
        """Skims the data into the output folder"""
        with utils.cd("data"):
            ds = {name: sources.Source(name, collection) for
                  name, collection in self.config_base.items()}

        with utils.cd("output"):
            [source.skim() for source in ds.values()]

        # CCMI-1 data skim asserts
        self.assertTrue(os.path.isdir("output/CCMI-1_IPSL"))
        self.assertTrue(os.path.exists("output/CCMI-1_IPSL/tco3_zm_2000.nc"))
        self.assertTrue(os.path.exists("output/CCMI-1_IPSL/vmro3_zm_2000.nc"))

        # ECMWF data skim asserts
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-5"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-5/tco3_zm_2000.nc"))
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-i"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/tco3_zm_2000.nc"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/vmro3_zm_2000.nc"))

        # Checks the original data has not been modified
        self.assert_with_backup()
        # Removes output data for other tests
        self.clean_output()

    def test_003_SourceErrorDontBreak(self):
        """The execution does not stop by an error in source"""
        with utils.cd("data"):
            ds = {name: sources.Source(name, collection) for
                  name, collection in self.config_err.items()}

        with utils.cd("output"):
            [source.skim() for source in ds.values()]

        # ECMWF data skim asserts
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-i"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/vmro3_zm_2000.nc"))

        # Checks the original data has not been modified
        self.assert_with_backup()
        # Removes output data for other tests
        self.clean_output()
