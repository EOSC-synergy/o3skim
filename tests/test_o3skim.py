"""Unittest module template."""


import os
import unittest

from o3skim import sources
# from pyfakefs.fake_filesystem_unittest import TestCase
from . import mockup_data


class TestO3SKIM_sources(unittest.TestCase):
    """Tests for `sources` package."""

    def setUp(self):
        """Loads and creates the test folders and files from test_sources.yaml"""
        self.config = sources.load("tests/test_sources.yaml")
        self.assertTrue(type(self.config) is dict)

        for source, collection in self.config.items():
            for model, variables in collection.items():
                for v, vinfo in variables.items():
                    path = "data/" + vinfo["dir"]
                    os.makedirs(path, exist_ok=True)
                    for n in range(3):
                        file_path = path + "/source_file_" + str(n) + ".nc"
                        mockup_data.netcdf(file_path, **vinfo)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        self.assertTrue(True)
        self.assertFalse(False)
