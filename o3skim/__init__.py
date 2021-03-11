"""O3as package with utilities to handle ozone data skimming."""
from o3skim import operations
import logging
import xarray as xr

logger = logging.getLogger('o3skim')


def process(dataset, actions):
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
        processed = process(processed, actions)
    return processed


def save(dataset, target, split_by=None):
    """Function in charge of saving the input dataset into the file
    system using an specified time range. The available type of
    output file formats are:

        :`None`: Output file format is {target}.nc
        :year:   Output file format is {target}_{y}-{y+01}.nc
        :decade: Output file format is {target}_{y}-{y+10}.nc

    :param dataset: DataSet to save in the target.
    :type dataset: :class:`xarray.DataSet`

    :param target: Location where to save followed by the name prefix. 
    :type target: str

    :param split_by: Type of saving format to apply.
    :type split_by:  str, optional
    """
    if not split_by:
        def path(_): return "{}.nc".format(target)
        groups = [(None, dataset)]
    elif split_by == 'year':
        def path(y): return "{}_{}-{}.nc".format(target, y, y + 1)
        def delta_map(x): return x.year
        years = dataset.indexes['time'].map(delta_map)
        groups = dataset.groupby(xr.DataArray(years))
    elif split_by == 'decade':
        def path(y): return "{}_{}-{}.nc".format(target, y, y + 10)
        def delta_map(x): return x.year // 10 * 10
        years = dataset.indexes['time'].map(delta_map)
        groups = dataset.groupby(xr.DataArray(years))
    else:
        message = "Bad input split_by '{}' use None, 'year' or 'decade'"
        raise KeyError(message.format(split_by))
    years, datasets = tuple(zip(*groups))
    try:
        xr.save_mfdataset(
            mode='a',
            datasets=[dataset for dataset in datasets],
            paths=[path(year) for year in years])
    except FileNotFoundError:
        xr.save_mfdataset(
            mode='w',
            datasets=[dataset for dataset in datasets],
            paths=[path(year) for year in years])
