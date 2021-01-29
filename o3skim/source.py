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
    r"""Conceptual class for a data source. It is produced by the 
    loading and standardization of multiple data models.

    The current supported model variables are "tco3_zm" and "vmro3_zm", 
    which should contain the information on how to retrieve the data
    from the netCDF collection.

    :param name: Name to provide to the source. 
    :type name: str

    :param metadata: Source metadata, defaults to {}.
    :type metadata: dict, optional

    :param \**collections: kwarg where each 'key' is the model 
        name and its 'value' another dictionary with the variable 
        loading statements for that model.
        {name:str, paths: str, coordinates: dict, metadata: dict} 
    """

    def __init__(self, name, metadata={}, **collections):
        self._name = name
        self._metadata = metadata
        self._models = {}
        logger.info("Loading source '%s'", name)
        for name, specifications in collections.items():
            logger.info("Loading model '%s'", name)
            model = _load_model(**specifications)
            if model:
                self._models[name] = model

    def __getitem__(self, model_name):
        return self._models[model_name]

    @property
    def name(self):
        return self._name

    @property
    def models(self):
        return list(self._models.keys())

    @property
    def metadata(self):
        return self._metadata

    def skim(self, groupby=None):
        """Request to skim all source data into the current folder.

        The output is generated into multiple folder where
        each model output is generated in a forder with the source
        name defined at the source initialization followed by 
        '_' and the model name: "<source_name>_<model_name>".
        If there was metadata added when creating the source, it is
        delivered into a "metadata.yaml" file on the directory.

        :param groupby: How to group output (None, 'year', 'decade').
        :type groupby: str, optional
        """
        for model in self._models:
            dirname = "{}_{}".format(self._name, model)
            os.makedirs(dirname, exist_ok=True)
            logger.info("Skimming data from '%s'", dirname)
            with utils.cd(dirname):
                metadata = {}  # copy() does not recurse inside dict
                utils.mergedicts(metadata, self.metadata)
                utils.mergedicts(metadata, self[model].model.metadata)
                _skim(self[model], delta=groupby, metadata=metadata)


@utils.return_on_failure("Error when loading model", default=None)
def _load_model(tco3_zm=None, vmro3_zm=None, metadata={}):
    """Loads a model merging standardized data from specified datasets.

    :param tco3_zm: tco3 variable description, defaults to None.
    :type tco3_zm: {name:str, paths:str, 
                    coordinates:{lat:str, lon:str, time:str}}, 
                    optional

    :param vmro3_zm: vmro3 variable description, defaults to None.
    :type vmro3_zm: {name:str, paths:str, 
                    coordinates:{lat:str, lon:str, plev:str time:str}}, 
                    optional

    :param metadata: Source metadata, defaults to {}.
    :type metadata: dict, optional

    :return: Dataset with specified variables.
    :rtype: xarray.Dataset
    """
    dataset = xr.Dataset()
    dataset.model.set_metadata(metadata)
    def raise_conflict(d1, d2): raise Exception(
        "Conflict merging {}, {}".format(d1, d2))
    if tco3_zm:
        logger.debug("Loading tco3_zm into model")
        with xr.open_mfdataset(tco3_zm['paths']) as load:
            dataset['tco3_zm'] = standardization.standardize_tco3(
                array=load[tco3_zm['name']],
                coordinates=tco3_zm['coordinates'])
            metadata = {'tco3_zm': tco3_zm.get('metadata', {})}
            dataset.model.add_metadata(metadata)
            utils.mergedicts(dataset.attrs, load.attrs, raise_conflict)
    if vmro3_zm:
        logger.debug("Loading vmro3_zm into model")
        with xr.open_mfdataset(vmro3_zm['paths']) as load:
            dataset['vmro3_zm'] = standardization.standardize_vmro3(
                array=load[vmro3_zm['name']],
                coordinates=vmro3_zm['coordinates'])
            metadata = {'vmro3_zm': vmro3_zm.get('metadata', {})}
            dataset.model.add_metadata(metadata)
            utils.mergedicts(dataset.attrs, load.attrs, raise_conflict)
    return dataset


def _skim(model, delta=None, metadata=None):
    """Skims model producing reduced dataset files. It is possible to
    indicate the time to split the output by 'delta'. If metadata is
    introduced in the form of dict, a 'metadata.yaml' file is 
    generated together with the skimmed output.

    :param model: Dataset with ModelAccessor to skim.
    :type model: xarray.Dataset

    :param metadata: Model metadata, to save as yaml defaults to None.
    :type metadata: dict, optional

    :param delta: How to group output (None, 'year', 'decade').
    :type delta:str, optional
    """
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
    if metadata:
        logger.debug("Creating metadata.yaml file")
        utils.save(file_name="metadata.yaml", metadata=metadata)
