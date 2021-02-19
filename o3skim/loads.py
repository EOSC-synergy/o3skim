"""
Module in charge of data loading and standardization.
"""
import datetime
import logging
import xarray as xr


logger = logging.getLogger('o3skim.loads')
strptime = datetime.datetime.strptime


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


def esacci(variable, time_parse, paths):
    def pf(ds):
        fpath = ds.encoding["source"]
        fname = fpath.split('/')[-1]
        fdate = fname.split('-')[-2]
        time = strptime(fdate, time_parse)
        return ds.expand_dims(time=[time])
    with xr.open_mfdataset(paths, preprocess=pf) as dataset:
        datarray = dataset[variable]
        ds_attrs = dataset.attrs
    return datarray, ds_attrs
