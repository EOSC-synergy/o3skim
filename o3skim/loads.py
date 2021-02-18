"""
Module in charge of data loading and standardizations.
"""
import logging
import xarray as xr


logger = logging.getLogger('o3skim.loads')


def ccmi(variable, paths):
    logger.debug("Loading CCMI-1 data from: %s", paths)
    with xr.open_mfdataset(paths) as dataset:
        datarray = dataset[variable]
        ds_attrs = dataset.attrs
    return datarray, ds_attrs


def ecmwf(variable, paths):
    logger.debug("Loading ECMWF data from: %s", paths)
    with xr.open_mfdataset(paths) as dataset:
        datarray = dataset[variable]
        ds_attrs = dataset.attrs
    return datarray, ds_attrs
