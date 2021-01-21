"""
Main package with classes and utilities to handle ozone data skimming.

Sources are responsible of loading the netCDF files from data and do
the standardization during the process.

After the data are loaded and the instances created,
it is possible to use the internal methods to produce
the desired output.
"""

import logging
import os
import unittest

import xarray as xr
import pandas as pd
import numpy as np
from o3skim import extended_xarray
from o3skim import standardization
from o3skim import utils

logger = logging.getLogger('o3skim')


class Source:
    """Conceptual class for a data source. It is produced by the loading
    and generation of internal instances from each data source model.

    :param name: Name to provide to the source. The folder name with the
        skimmed output data is preceded with this name before '_'.
    :type name: str

    :param collections: Dictionary where each 'key' is a name and its
        value another dictionary with the variables contained at this
        model. See :class:`o3skim.Model` for further details.
    :type collections: dict
    """

    def __init__(self, name, collections):
        self.name = name
        self._models = {}
        logging.info("Load source '%s'", self.name)
        for name, specifications in collections.items():
            logging.info("Load model '%s'", name)
            model = __load_model(**specifications)
            if model:
                self._models[name] = model

    def __getitem__(self, model_name):
        return self._models[model_name]

    @property
    def models(self):
        return self._models.keys()

    def skim(self, groupby=None):
        """Request to skim all source data into the current folder

        :param groupby: How to group output (None, year, decade).
        :type groupby: str, optional
        """
        for model in self._models:
            dirname = "{source}_{model}".format(source=self.name, model=model)
            os.makedirs(dirname, exist_ok=True)
            logger.info("Skim data from '%s'", dirname)
            with utils.cd(dirname):
                Skimmed_ds = self[model].model.skim()
                Skimmed_ds.to_netcdf(groupby)


@utils.return_on_failure("Error when loading model", default=None)
def __load_model(tco3_zm=None, vmro3_zm=None):
    """Loads and standarises a dataset using the specs."""
    dataset = xr.Dataset()
    if tco3_zm:
        with xr.open_mfdataset(tco3_zm['paths']) as load:
            standardized = standardization.standardize_tco3(
                dataset=load,
                variable=tco3_zm['name'],
                coordinates=tco3_zm['coordinates'])
            dataset = dataset.merge(standardized)
    if vmro3_zm:
        with xr.open_mfdataset(vmro3_zm['paths']) as load:
            standardized = standardization.standardize_vmro3(
                dataset=load,
                variable=vmro3_zm['name'],
                coordinates=vmro3_zm['coordinates'])
            dataset = dataset.merge(standardized)
    return dataset


class TestsSource(unittest.TestCase):

    name = "SourceTest"
    collections = {}  # Empty, only to test constructor stability

    def setUp(self):
        self.source = Source(TestsSource.name, TestsSource.collections)

    def test_property_name(self):
        expected = TestsSource.name
        result = self.source.name
        self.assertEqual(expected, result)

    def test_property_models(self):
        expected = TestsSource.collections.keys()
        result = self.source.models
        self.assertEqual(expected, result)


class TestsModel(unittest.TestCase):

    tco3 = np.random.rand(3, 3, 25)
    vmro3 = np.random.rand(3, 3, 4, 25)

    @ staticmethod
    def model():
        return xr.Dataset(
            data_vars=dict(
                tco3_zm=(["lon", "lat", "time"], TestsModel.tco3),
                vmro3_zm=(["lon", "lat", "plev", "time"], TestsModel.vmro3)
            ),
            coords=dict(
                lon=[-180, 0, 180],
                lat=[-90, 0, 90],
                plev=[1, 10, 100, 1000],
                time=pd.date_range("2000-01-01", periods=25, freq='A')
            ),
            attrs=dict(description="Test dataset")
        )

    def assertHasAttr(self, obj, intendedAttr):
        testBool = hasattr(obj, intendedAttr)
        msg = 'obj lacking an attribute. obj: %s, intendedAttr: %s' % (
            obj, intendedAttr)
        self.assertTrue(testBool, msg=msg)

    def test_dataset_has_model_accessor(self):
        model = TestsModel.model()
        self.assertHasAttr(model, 'model')
        xr.testing.assert_equal(model["tco3_zm"], model.model.tco3)
        xr.testing.assert_equal(model["vmro3_zm"], model.model.vmro3)
