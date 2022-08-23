"""O3as package with utilities to handle ozone data skimming."""
import logging

import cf_xarray as cfxr
import xarray as xr

import o3skim.loadfunctions_tco3 as loadfunctions_tco3
import o3skim.loadfunctions_zmo3 as loadfunctions_zmo3

logger = logging.getLogger("o3skim")
xr.set_options(keep_attrs=True)


def load_tco3(path, model):
    """Module in charge of standardized data model loading for tco3.
    :param path: Expression with netcdf files containing the model
    :param model: Name of model
    :return: Standardized loaded dataset
    """
    load = __model_loader(loadfunctions_tco3, model).load_tco3
    return load(path)


def load_zmo3(path, model):
    """Module in charge of standardized data model loading for zmo3.
    :param path: Expression with netcdf files containing the model
    :param model: Name of model
    :return: Standardized loaded dataset
    """
    load = __model_loader(loadfunctions_zmo3, model).load_zmo3
    return load(path)


def __model_loader(package, model):
    modules = [m for m in package.__all__ if m in model]
    if len(modules) == 1:
        return package.__dict__[modules[0]]
    if modules == []:
        raise ValueError(f"Unknown model '{model}' from {package.__all__}")
    elif modules.len > 1:
        raise ValueError(f"Multiple match '{model}' for {modules}")


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

    # Return dataset with renamed variables adding '_zm' at the end
    return dataset.rename({var: f"{var}_zm" for var in dataset.data_vars})


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

    # Return dataset TODO: Rename variables adding '_??' at the end
    return dataset
