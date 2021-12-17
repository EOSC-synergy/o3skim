"""Module in charge of implementing the o3skim operations."""
import logging

import cf_xarray as cfxr
import xarray as xr

logger = logging.getLogger("o3skim.operations")
xr.set_options(keep_attrs=True)  # Keep attributes
toz_standard_name = "atmosphere_mole_content_of_ozone"


def run(dataset, operation):
    """Main entry point for operation call on o3skimming functions:

        :lon_mean:  Longitudinal mean across the dataset.
        :lat_mean:  Latitudinal mean across the dataset.
        :year_mean: Time coordinate averaged by year.

    :param dataset: Original o3 dataset where to perform operations.
    :type dataset: :class:`xarray.Dataset`

    :param operation: Operation name to perform.
    :type operation: str

    :return: Dataset after processing the specified operation.
    :rtype: :class:`xarray.Dataset`
    """
    if operation == "lon_mean":
        return lon_mean(dataset)
    elif operation == "lat_mean":
        return lat_mean(dataset)
    elif operation == "year_mean":
        return year_mean(dataset)
    else:
        err = "Bad selected operation: {}"
        raise KeyError(err.format(operation))


def lon_mean(dataset):
    logger.debug("Calculating mean over model longitude")
    result = dataset.cf.mean("longitude")

    __fix_area_mean(result, toz_standard_name)
    return result


def lat_mean(dataset):
    logger.debug("Calculating mean over model latitude")
    result = dataset.cf.mean("latitude")

    __fix_area_mean(result, toz_standard_name)
    return result


def year_mean(dataset):
    logger.debug("Calculating mean over time by year")
    result = dataset.cf.resample(T="Y").mean()

    method = "time: mean (interval: 1 years)"
    __append_method(result, toz_standard_name, method)
    return result


def __fix_area_mean(dataset, variable):
    for var_name in ["lat", "lon", "latitude", "longitude"]:
        method = var_name + ": mean "
        __delete_method(dataset, variable, method)

    __append_method(dataset, variable, "area: mean")


def __append_method(dataset, variable, method):
    var_name = dataset.cf[variable].name
    var_attrs = dataset[var_name].attrs
    cell_methods = dataset[var_name].cell_methods

    var_attrs["cell_methods"] = cell_methods + " " + method


def __delete_method(dataset, variable, method):
    var_name = dataset.cf[variable].name
    var_attrs = dataset[var_name].attrs
    cell_methods = dataset[var_name].cell_methods

    var_attrs["cell_methods"] = cell_methods.replace(method + " ", "")
