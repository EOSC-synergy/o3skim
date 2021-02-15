"""
Module in charge of implementing the o3skim operations.
"""
import logging

logger = logging.getLogger('o3skim.operations')


def run(name, dataset):
    """Main entry point for operation call on o3skimming functions:

        :lon_mean: Longitudinal mean accross the dataset.
        :lat_mean: Latitudinal mean accross the dataset.

    :param name: Operation name to perform. 
    :type name: str

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`xarray.Dataset`

    :return: Dataset after processing the specified operation.
    :rtype: :class:`xarray.Dataset`
    """
    if name == 'lon_mean':
        return lon_mean(dataset)
    elif name == 'lat_mean':
        return lat_mean(dataset)
    else:
        message = "Bad selected operation: {}"
        raise KeyError(message.format(name))


def lon_mean(dataset):
    logger.debug("Calculating mean over model longitude")
    skimmed = dataset.mean('lon')
    skimmed.attrs = dataset.attrs
    for var in dataset.var():
        skimmed[var].attrs = dataset[var].attrs
    return skimmed


def lat_mean(dataset):
    logger.debug("Calculating mean over model latitude")
    skimmed = dataset.mean('lat')
    skimmed.attrs = dataset.attrs
    for var in dataset.var():
        skimmed[var].attrs = dataset[var].attrs
    return skimmed
