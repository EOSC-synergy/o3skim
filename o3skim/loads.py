"""
Module in charge of data loading and standardization.
"""
import pandas as pd
import numpy as np
import logging
import xarray as xr
import o3skim.utils as utils


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


def esacci(variable, time_position, paths):
    def pf(ds):
        fpath = ds.encoding["source"]
        fname = fpath.split('/')[-1]
        fdate = fname.split('-')[time_position]
        time = pd.to_datetime(fdate)
        return ds.expand_dims(time=[time])
    with xr.open_mfdataset(paths, preprocess=pf) as dataset:
        datarray = dataset[variable]
        ds_attrs = dataset.attrs
    return datarray, ds_attrs


def sbuv(textfile, delimiter):
    with open(textfile, 'r') as strio:
        tables = utils.chunkio('SBUV', strio)
    arrays = []
    for head, chunk in tables:
        header = head[0:-2].split(' ')
        year = int(header[0])
        table = pd.read_table(chunk, sep=delimiter, index_col=[0, 1])
        table.index = [(int(l1)+int(l2))/2 for l1, l2 in table.index]
        array = xr.DataArray(
            data=table,
            attrs=dict(
                version=header[3],
                name=header[1],
                description=' '.join(header[-3:])),
            dims=['lat', 'time'],
            coords=dict(
                lat=table.index,
                time=[pd.datetime(year, m, 1) for m in range(1, 13)]))
        array.values.flat[array.values.flat == 0.0] = np.nan
        arrays.append(array)
    return xr.concat(arrays, 'time'), {}
