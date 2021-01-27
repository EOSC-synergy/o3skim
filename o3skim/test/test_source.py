import unittest

import pandas as pd
import numpy as np
import xarray as xr
from o3skim import source

Source = source.Source

name = "SourceTest"
collections = {}  # Empty, only to test constructor stability


class TestsSource(unittest.TestCase):

    def setUp(self):
        self.source = Source(name, collections)

    def test_property_name(self):
        self.assertEqual(name, self.source.name)

    def test_property_models(self):
        expected = list(collections.keys())
        result = self.source.models
        self.assertEqual(expected, result)
