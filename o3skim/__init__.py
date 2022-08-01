"""O3as package with utilities to handle ozone data skimming."""
import logging

import cf_xarray as cfxr
import xarray as xr

from o3skim import loadfunctions_tco3

logger = logging.getLogger("o3skim")
xr.set_options(keep_attrs=True)


def load_tco3(path, source, model):
    """Module in charge of standardized data model loading.
    :param path: Expresion with netcdf files containing the model
    :param source: Name of model source
    :param model: Name of model
    :return: Standardized loaded dataset
    """
    source_package = __source_loader(loadfunctions_tco3, source)
    load = __model_loader(source_package, model).load_tco3
    return load(path)


def __source_loader(package, source):
    try:
        return package.__dict__[source]
    except KeyError:
        raise ValueError(f"Unknown source '{source}'")


def __model_loader(package, model):
    try:
        return package.__dict__[model]
    except KeyError:
        raise ValueError(f"Unknown model '{model}'")


def lon_mean(dataset):
    """Longitudinal mean across the dataset following CF conventions.
    :param dataset: xarray.dataset following CF conventions
    :return: xarray.dataset
    """
    logger.debug("Calculating mean over model longitude")
    bounds = dataset.cf["longitude"].attrs.get("bounds", None)
    dataset = dataset.cf.mean("longitude")

    # Dirty code: cell-methods patch
    # See https://github.com/xarray-contrib/cf-xarray/discussions/314
    for var in dataset.data_vars:
        if "cell_methods" in dataset[var].attrs:
            dataset[var].attrs["cell_methods"] += " longitude: mean"

    # Remove bounds if not removed
    dataset = dataset.cf.drop_vars(bounds) if bounds else dataset

    return dataset


def lat_mean(dataset):
    """Latitudinal mean across the dataset following CF conventions.
    :param dataset: xarray.dataset following CF conventions
    :return: xarray.dataset
    """
    logger.debug("Calculating mean over model latitude")
    bounds = dataset.cf["latitude"].attrs.get("bounds", None)
    dataset = dataset.cf.mean("latitude")

    # Dirty code: cell-methods patch
    # See https://github.com/xarray-contrib/cf-xarray/discussions/314
    for var in dataset.data_vars:
        if "cell_methods" in dataset[var].attrs:
            dataset[var].attrs["cell_methods"] += " latitude: mean"

    # Remove bounds if not removed
    dataset = dataset.cf.drop_vars(bounds) if bounds else dataset

    return dataset
