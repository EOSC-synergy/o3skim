"""Module in charge of implementing the o3skim operations."""
import logging
import pandas as pd

logger = logging.getLogger('o3skim.operations')


def run(name, dataset):
    """Main entry point for operation call on o3skimming functions:

        :lon_mean:  Longitudinal mean across the dataset.
        :lat_mean:  Latitudinal mean across the dataset.
        :year_mean: Time coordinate averaged by year.

    :param name: Operation name to perform.
    :type name: str

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`xarray.Dataset`

    :return: Dataset after processing the specified operation.
    :rtype: :class:`xarray.Dataset`
    """
    if name == 'lon_mean':
        return _lon_mean(dataset)
    elif name == 'lat_mean':
        return _lat_mean(dataset)
    elif name == 'year_mean':
        return _year_mean(dataset)
    else:
        message = "Bad selected operation: {}"
        raise KeyError(message.format(name))


def _lon_mean(dataset):
    logger.debug("Calculating mean over model longitude")
    skimmed = dataset.mean('lon')
    skimmed.attrs = dataset.attrs
    for var in dataset.var():
        skimmed[var].attrs = dataset[var].attrs
    return skimmed


def _lat_mean(dataset):
    logger.debug("Calculating mean over model latitude")
    skimmed = dataset.mean('lat')
    skimmed.attrs = dataset.attrs
    for var in dataset.var():
        skimmed[var].attrs = dataset[var].attrs
    return skimmed


def _year_mean(dataset):
    logger.debug("Calculating mean over time by year")
    skimmed = dataset.groupby('time.year').mean('time')
    newtime = [pd.datetime(y, 7, 2) for y in skimmed.year]
    skimmed = skimmed.assign_coords(year=newtime)
    skimmed = skimmed.rename({'year': 'time'})
    skimmed.attrs = dataset.attrs
    for var in dataset.var():
        skimmed[var].attrs = dataset[var].attrs
    return skimmed
