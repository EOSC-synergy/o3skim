"""
Module in charge of operations implementation.
"""
import logging

logger = logging.getLogger('operations')


def run(name, dataset):
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
