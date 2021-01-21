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

from o3skim import extended_xarray
from o3skim import standardization
from o3skim import utils
import xarray as xr

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
        self.models = [x for x in collections.keys()]
        self._models = {}
        logging.info("Load source '%s'", self.name)
        for name, specifications in collections.items():
            logging.info("Load model '%s'", name)
            model = __load_model(**specifications)
            if model:
                self._models[name] = model 

    def __getitem__(self, model_name):
        return self._models[model_name]

    def skim(self, groupby=None):
        """Request to skim all source data into the current folder

        :param groupby: How to group output (None, year, decade).
        :type groupby: str, optional
        """
        for model in self.models:
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
