"""Module in charge of implementing the o3skim operations."""
import logging

import cf_xarray as cfxr

logger = logging.getLogger("o3skim.operations")


def run(operation, dataset):
    """Main entry point for operation call on o3skimming functions:

        :lon_mean:  Longitudinal mean across the dataset.
        :lat_mean:  Latitudinal mean across the dataset.
        :year_mean: Time coordinate averaged by year.

    :param operation: Operation name to perform.
    :type operation: str

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`xarray.Dataset`

    :return: Dataset after processing the specified operation.
    :rtype: :class:`xarray.Dataset`
    """
    if operation == "lon_mean":
        return _lon_mean(dataset)
    elif operation == "lat_mean":
        return _lat_mean(dataset)
    elif operation == "year_mean":
        return _year_mean(dataset)
    else:
        err = "Bad selected operation: {}"
        raise KeyError(err.format(operation))


def _lon_mean(dataset):
    logger.debug("Calculating mean over model longitude")
    result = dataset.cf.mean("longitude")

    return result


def _lat_mean(dataset):
    logger.debug("Calculating mean over model latitude")
    result = dataset.cf.mean("latitude")

    return result


def _year_mean(dataset):
    logger.debug("Calculating mean over time by year")
    result = dataset.cf.resample(T="Y").mean()

    return result
