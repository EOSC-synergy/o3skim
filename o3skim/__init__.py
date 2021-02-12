"""
O3as package with classes and utilities to handle ozone data skimming.
"""
import logging
import xarray as xr

from o3skim import loads
from o3skim import operations
from o3skim import utils
from o3skim import extended_xarray

logger = logging.getLogger('o3skim')


def loading(tco3_zm=None, vmro3_zm=None, metadata={}):
    logger.debug("Loading ozone variables data")
    dataset = xr.Dataset()
    def raise_conflict(d1, d2): raise Exception(
        "Conflict merging {}, {}".format(d1, d2))
    if tco3_zm:
        datarray, ds_attrs, meta = loads.tco3(**tco3_zm)
        dataset['tco3_zm'] = datarray
        utils.mergedicts(dataset.attrs, ds_attrs, raise_conflict)
        metadata['tco3_zm'] = meta
    if vmro3_zm:
        datarray, ds_attrs, meta = loads.vmro3(**vmro3_zm)
        dataset['vmro3_zm'] = datarray
        utils.mergedicts(dataset.attrs, ds_attrs, raise_conflict)
        metadata['vmro3_zm'] = meta
    return dataset, metadata


def processing(dataset, actions):
    logger.debug("Processing queue: %s", actions)
    actions = actions.copy() # Do not edit original
    operation = actions.pop()
    processed = operations.run(operation, dataset)
    if actions != []:
        processed = processing(processed, actions)
    return processed


def group(dataset, split_by):
    logger.debug("Splitting dataset by %s", split_by)
    if not split_by:
        return [None], [dataset]
    elif split_by == 'year':
        def delta_map(x): return x.year
        years = dataset.indexes['time'].map(delta_map)
        groups = dataset.groupby(xr.DataArray(years))
    elif split_by == 'decade':
        def delta_map(x): return x.year // 10 * 10
        years = dataset.indexes['time'].map(delta_map)
        groups = dataset.groupby(xr.DataArray(years))
    else:
        message = "Bad input split_by {} use {None, 'year', 'decade'}"
        raise KeyError(message.format(split_by))
    return tuple(zip(*groups))


def saving(datasets, split_by=None, years=None):
    if not split_by:
        def path(v, _): return "{}.nc".format(v)
    elif split_by == 'year':
        def path(v, y): return "{}_{}-{}.nc".format(v, y, y + 1)
    elif split_by == 'decade':
        def path(v, y): return "{}_{}-{}.nc".format(v, y, y + 10)
    else:
        message = "Bad input split_by {} use {None, 'year', 'decade'}"
        raise KeyError(message.format(split_by))
    for variable in datasets[0].var():
        xr.save_mfdataset(
            datasets=[ds.o3[variable].dataset for ds in datasets],
            paths=[path(variable, year) for year in years])
