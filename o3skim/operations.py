"""Module in charge of implementing the o3skim operations."""
import logging

import cf_xarray as cfxr
import iris
import iris.coord_categorisation
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
    # dataset.coord('longitude').guess_bounds()  # Calc bounds if not pressent
    areas = iris.analysis.cartography.area_weights(dataset)
    result = dataset.collapsed("longitude", iris.analysis.MEAN, weights=areas)
    result.remove_coord("longitude")  # No need to include: CF 7.3.4
    return result


def lat_mean(dataset):
    logger.debug("Calculating mean over model latitude")
    # dataset.coord('latitude').guess_bounds()  # Calc bounds if not pressent
    areas = iris.analysis.cartography.area_weights(dataset)
    result = dataset.collapsed("latitude", iris.analysis.MEAN, weights=areas)
    result.remove_coord("latitude")  # No need to include: CF 7.3.4
    return result


def year_mean(dataset):
    logger.debug("Calculating mean over time by year")
    iris.coord_categorisation.add_year(dataset, 'time', name='year')
    result = dataset.aggregated_by(['year'], iris.analysis.MEAN)
    return result

