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
    message = "Calculating '{}' over model"
    logger.debug(message.format(operation))
    if operation == "lon_mean":
        return dataset.cf.mean("longitude")
    elif operation == "lat_mean":
        return dataset.cf.mean("latitude")
    elif operation == "year_mean":
        return dataset.cf.resample(T="Y").mean()
    else:
        err = "Bad selected operation: {}"
        raise KeyError(err.format(operation))
