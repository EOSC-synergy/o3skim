"""Unittest module template."""

import os
import shutil
import unittest
import glob

import o3skim
import xarray as xr

from tests import mockup_data
from tests import mockup_noise


class TestO3SKIM_sources(unittest.TestCase):
    """Tests for `sources` package."""

    def setUp(self):
        """Loads and creates the test folders and files from test_sources.yaml"""
        self.config_base = o3skim.utils.load("tests/sources_base.yaml")
        self.assertTrue(type(self.config_base) is dict)
        self.config_err = o3skim.utils.load("tests/sources_err.yaml")
        self.assertTrue(type(self.config_err) is dict)

        self.create_mock_datasets()
        self.backup_datasets()
        self.assert_with_backup()
        self.create_noise_datasets()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def create_mock_datasets(self):
        """Creates mock data files according to the loaded configuration"""
        with o3skim.utils.cd('data'):
            for _, collection in self.config_base.items():
                for _, variables in collection.items():
                    for _, vinfo in variables.items():
                        dirname = os.path.dirname(vinfo['paths'])
                        os.makedirs(dirname, exist_ok=True)
                        mockup_data.netcdf(dirname, **vinfo)

    def create_noise_datasets(self):
        """Creates noise data files according to the noise configuration"""
        config_noise = o3skim.utils.load("tests/noise_files.yaml")
        with o3skim.utils.cd('data'):
            for ninfo in config_noise:
                mockup_noise.netcdf(**ninfo)

    def clean_output(self):
        """Cleans output removing all folders at output"""
        with o3skim.utils.cd('output'):
            directories = (d for d in os.listdir() if os.path.isdir(d))
            for directory in directories:
                shutil.rmtree(directory)

    def backup_datasets(self):
        """Loads the mock datasets into an internal variable"""
        self.ds_backup = {}
        with o3skim.utils.cd('data'):
            for source, collection in self.config_base.items():
                self.ds_backup[source] = {}
                for model, variables in collection.items():
                    self.ds_backup[source][model] = {}
                    for v, vinfo in variables.items():
                        with xr.open_mfdataset(vinfo['paths']) as ds:
                            self.ds_backup[source][model][v] = ds

    def assert_with_backup(self):
        """Asserts the dataset in the backup is equal to the config load"""
        with o3skim.utils.cd('data'):
            for source, collection in self.config_base.items():
                for model, variables in collection.items():
                    for v, vinfo in variables.items():
                        with xr.open_mfdataset(vinfo['paths']) as ds:
                            xr.testing.assert_identical(
                                self.ds_backup[source][model][v], ds)

    def test_001_SourcesFromConfig(self):
        """Creates the different sources from the configuration file"""
        with o3skim.utils.cd("data"):
            ds = {name: o3skim.Source(name, collection) for
                  name, collection in self.config_base.items()}

        # CCMI-1 tco3_zm asserts
        self.assertTrue( 'time' in ds['CCMI-1']._models['IPSL']['tco3_zm'].coords)
        self.assertTrue( 'lat' in ds['CCMI-1']._models['IPSL']['tco3_zm'].coords)
        self.assertFalse( 'lon' in ds['CCMI-1']._models['IPSL']['tco3_zm'].coords)

        # CCMI-1 vmro3_zm asserts
        self.assertTrue( 'time' in ds['CCMI-1']._models['IPSL']['vmro3_zm'].coords)
        self.assertTrue( 'plev' in ds['CCMI-1']._models['IPSL']['vmro3_zm'].coords)
        self.assertTrue( 'lat' in ds['CCMI-1']._models['IPSL']['vmro3_zm'].coords)
        self.assertFalse( 'lon' in ds['CCMI-1']._models['IPSL']['vmro3_zm'].coords)

        # Checks the original data has not been modified
        self.assert_with_backup()

    def test_002_OutputFromSources(self):
        """Skims the data into the output folder"""
        with o3skim.utils.cd("data"):
            ds = {name: o3skim.Source(name, collection) for
                  name, collection in self.config_base.items()}

        with o3skim.utils.cd("output"):
            [source.skim() for source in ds.values()]

        # CCMI-1 data skim asserts
        self.assertTrue(os.path.isdir("output/CCMI-1_IPSL"))
        self.assertTrue(os.path.exists("output/CCMI-1_IPSL/tco3_zm.nc"))
        self.assertTrue(os.path.exists("output/CCMI-1_IPSL/vmro3_zm.nc"))

        # ECMWF data skim asserts
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-5"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-5/tco3_zm.nc"))
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-i"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/tco3_zm.nc"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/vmro3_zm.nc"))

        # Checks the original data has not been modified
        self.assert_with_backup()
        # Removes output data for other tests
        self.clean_output()

    def test_003_OutputSplitByYear(self):
        """Skims the data into the output folder spliting by year"""
        with o3skim.utils.cd("data"):
            ds = {name: o3skim.Source(name, collection) for
                  name, collection in self.config_base.items()}

        with o3skim.utils.cd("output"):
            [source.skim(groupby="year") for source in ds.values()]

        # CCMI-1 data skim asserts
        self.assertTrue(os.path.isdir("output/CCMI-1_IPSL"))
        self.assertTrue(os.path.exists("output/CCMI-1_IPSL/tco3_zm_2000-2001.nc"))
        self.assertTrue(os.path.exists("output/CCMI-1_IPSL/vmro3_zm_2000-2001.nc"))

        # ECMWF data skim asserts
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-5"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-5/tco3_zm_2000-2001.nc"))
        self.assertTrue(os.path.isdir("output/ECMWF_ERA-i"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/tco3_zm_2000-2001.nc"))
        self.assertTrue(os.path.exists("output/ECMWF_ERA-i/vmro3_zm_2000-2001.nc"))

        # Checks the original data has not been modified
        self.assert_with_backup()
        # Removes output data for other tests
        self.clean_output()

    def test_004_SourceErrorDontBreak(self):
        """The execution does not stop by an error in source"""
        with o3skim.utils.cd("data"):
            ds = {name: o3skim.Source(name, collection) for
                  name, collection in self.config_err.items()}

        with o3skim.utils.cd("output"):
            [source.skim() for source in ds.values()]

        # ECMWF data skim asserts
        self.assertTrue(os.path.isdir("output/ErrorModels_correct_variable"))
        self.assertTrue(os.path.exists( "output/ErrorModels_correct_variable/vmro3_zm.nc"))
        self.assertTrue(os.path.isdir( "output/ErrorModels_non_existing_variable"))
        self.assertTrue( len(os.listdir("output/ErrorModels_non_existing_variable")) == 0)
        # self.assertTrue(os.path.isdir("output/ECMWF_wrong_coordinates"))
        # self.assertTrue(len(os.listdir("output/ECMWF_wrong_coordinates")) == 0)

        # Checks the original data has not been modified
        self.assert_with_backup()
        # Removes output data for other tests
        self.clean_output()
