"""
Module in charge of Source class implementation.

Sources are responsible of loading netCDF collections from data and 
do the standardization during the process. Each source is compose
therefore from 0 to N models which can be accessed as subscriptable
object by it's model name.

It also implement internal methods which can be used to operate the
model data. For example using the method "skim" generates a reduced
version of the models data on the current folder.
"""

import logging
import os
import unittest

import pandas as pd
import numpy as np
import xarray as xr
from o3skim import extended_xarray
from o3skim import standardization
from o3skim import utils

logger = logging.getLogger('source')


class Source:
    """Conceptual class for a data source. It is produced by the loading
    and standardization of multiple data models.

    The current supported model variables are "tco3_zm" and "vmro3_zm", 
    which should contain the information on how to retrieve the data
    from the netCDF collection.
     
    :param name: Name to provide to the source. 
    :type name: str

    :param collections: Dictionary where each 'key' is a model name 
        and its value another dictionary with the variable loading 
        statements for that model.
        {name:str, paths: str, coordinates: dict} 
    :type collections: dict
    """

    def __init__(self, name, collections):
        self.name = name
        self._models = {}
        logger.info("Loading source '%s'", self.name)
        for name, specifications in collections.items():
            logger.info("Loading model '%s'", name)
            model = _load_model(**specifications)
            if model:
                self._models[name] = model

    def __getitem__(self, model_name):
        return self._models[model_name]

    @property
    def models(self):
        return list(self._models.keys())

    def skim(self, groupby=None):
        """Request to skim all source data into the current folder.

        The output is generated into multiple folder where
        each model output is generated in a forder with the source
        name defined at the source initialization followed by 
        '_' and the model name: "<source_name>_<model_name>"

        :param groupby: How to group output (None, 'year', 'decade').
        :type groupby: str, optional
        """
        for model in self._models:
            dirname = "{source}_{model}".format(source=self.name, model=model)
            os.makedirs(dirname, exist_ok=True)
            logger.info("Skimming data from '%s'", dirname)
            with utils.cd(dirname):
                _skim(self[model], delta=groupby)


@utils.return_on_failure("Error when loading model", default=None)
def _load_model(tco3_zm=None, vmro3_zm=None):
    """Loads a model merging standardized data from specified datasets."""
    dataset = xr.Dataset()
    if tco3_zm:
        logger.debug("Loading tco3_zm into model")
        with xr.open_mfdataset(tco3_zm['paths']) as load:
            standardized = standardization.standardize_tco3(
                dataset=load,
                variable=tco3_zm['name'],
                coordinates=tco3_zm['coordinates'])
            dataset = dataset.merge(standardized)
    if vmro3_zm:
        logger.debug("Loading vmro3_zm into model")
        with xr.open_mfdataset(vmro3_zm['paths']) as load:
            standardized = standardization.standardize_vmro3(
                dataset=load,
                variable=vmro3_zm['name'],
                coordinates=vmro3_zm['coordinates'])
            dataset = dataset.merge(standardized)
    return dataset


def _skim(model, delta=None):
    """Skims model producing reduced dataset files"""
    logger.debug("Skimming model with delta {}".format(delta))
    skimmed = model.model.skim()
    if delta == 'year':
        def tco3_path(y): return "tco3_zm_{}-{}.nc".format(y, y + 1)
        def vmro3_path(y): return "vmro3_zm_{}-{}.nc".format(y, y + 1)
        groups = skimmed.model.groupby_year()
    elif delta == 'decade':
        def tco3_path(y): return "tco3_zm_{}-{}.nc".format(y, y + 10)
        def vmro3_path(y): return "vmro3_zm_{}-{}.nc".format(y, y + 10)
        groups = skimmed.model.groupby_decade()
    else:
        def tco3_path(_): return "tco3_zm.nc"
        def vmro3_path(_): return "vmro3_zm.nc"
        groups = [(None, skimmed), ]
    years, datasets = zip(*groups)
    if skimmed.model.tco3:
        logger.debug("Saving skimed tco3 into files")
        xr.save_mfdataset(
            datasets=[ds.model.tco3 for ds in datasets],
            paths=[tco3_path(year) for year in years]
        )
    if skimmed.model.vmro3:
        logger.debug("Saving skimed vmro3 into files")
        xr.save_mfdataset(
            datasets=[ds.model.vmro3 for ds in datasets],
            paths=[vmro3_path(year) for year in years]
        )


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
        expected = list(TestsSource.collections.keys())
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