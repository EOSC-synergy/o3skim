"""
Module in charge of data loading.
"""
import logging

from o3skim import standardization
from o3skim import utils
import xarray as xr


logger = logging.getLogger('load')


def tco3(name, paths, coordinates, metadata={}):
    logger.debug("Loading tco3 data from: %s", paths)
    with xr.open_mfdataset(paths) as dataset:
        datarray = standardization.tco3(
            array=dataset[name],
            coord=coordinates)
        ds_attrs = dataset.attrs
    return datarray, ds_attrs, metadata


def vmro3(name, paths, coordinates, metadata={}):
    logger.debug("Loading vmro3 data from: %s", paths)
    with xr.open_mfdataset(paths) as dataset:
        datarray = standardization.vmro3(
            array=dataset[name],
            coord=coordinates)
        ds_attrs = dataset.attrs
    return datarray, ds_attrs, metadata
