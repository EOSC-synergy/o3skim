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
    """Function in charge of o3 variable data loading. The specifications 
    for the variables to load must follow this dict structure:

        :paths:         Regex expresion with paths to the datasets to load.
        :name:          Variable to retrieve after loading datasets.
        :coordinates:   Coordinates map translation from original datasets.
        :metadata:      Optional. Variable added metadata. 

    :param tco3_zm: Total Column Ozone data specifications.
    :type tco3_zm: dict, {paths, name, coordinates, metadata}

    :param vmro3_zm: Total Volume Mixing ratio data specifications.
    :type vmro3_zm: dict, {paths, name, coordinates, metadata}

    :param metadata: Model general metadata. Defaults to empty dict: {}.
    :type metadata: dict, optional

    :return: Xarray Dataset with specified variables and the metadata.
    :rtype: tuple (:class:`xarray.Dataset`, metadata: dict)
    """
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
    """Function in charge of processing the list of o3skim operations
    to the ozone variables dataset. The available list of operations
    to perform are:

        :lon_mean: Longitudinal mean accross the dataset.
        :lat_mean: Latitudinal mean accross the dataset.

    Note that multiple operations can be concatenated. For example
    using the list ['lon_mean', 'lat_mean'] as actions parameter 
    input would perform a longitudinal mean followed afterwards by
    a latitudinal mean before returning the result.

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`xarray.Dataset`

    :param actions: List of operation names to perform. 
    :type actions: list

    :return: Dataset after processing listed operations.
    :rtype: :class:`xarray.Dataset`
    """
    logger.debug("Processing queue: %s", actions)
    actions = actions.copy()  # Do not edit original
    operation = actions.pop()
    processed = operations.run(operation, dataset)
    if actions != []:
        processed = processing(processed, actions)
    return processed


def grouping(dataset, split_by):
    """Function in charge of splitting the input dataset into the 
    specified time range. The available list of split groups are:

        :`None`: No splitting, returns ([None], [dataset])
        :year:   Split accross the dataset years.
        :decade: Split accross the dataset decades.

    :param dataset: Original o3 dataset where to perform splitting.
    :type dataset: :class:`xarray.Dataset`

    :param split_by: Type of split to apply. 
    :type split_by: str or None

    :return: Dataset after splitting by the defined time.
    :rtype: tuple ([year], [:class:`xarray.Dataset`])
    """
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
    """Function in charge of saving the input dataset into the file
    system using an specified time range. The available type of 
    output file formats are:

        :`None`: Output file format is {var}.nc
        :year:   Output file format is {var}_{y}-{y+01}.nc
        :decade: Output file format is {var}_{y}-{y+10}.nc

    Note that dataset are saved in the current workspace directory.

    :param datasets: List o3 datasets to save in the filesystem.
    :type datasets: [:class:`xarray.Dataset`]

    :param split_by: Type of saving format to apply. 
    :type split_by:  str or None
    """
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
