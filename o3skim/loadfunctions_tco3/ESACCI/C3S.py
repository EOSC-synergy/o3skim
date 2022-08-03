import logging


import xarray as xr
from o3skim import config, utils

## Application logger
logger = logging.getLogger(__name__)


VARIABLE_NAME = "total_ozone_column"
CONVENTIONS = "CF-1.8"
INSTITUTION = "Copernicus Climate Change Service"
SOURCE = ""  # TODO: Define source


def load_tco3(model_path):
    """Loads and returns a ESACCI CS3 DataArray model and the dataset
    attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading ESACCI C3S data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Clean of non cf attributes
    utils.cf_clean(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Variable '{VARIABLE_NAME}' loading")
    bounds = [dataset[v].attrs.get("bounds", None) for v in dataset.coords]
    bounds = [bound for bound in bounds if bound is not None]
    keep_v = set([dataset.cf[VARIABLE_NAME].name] + bounds)
    drop_v = [v for v in dataset.data_vars if v not in keep_v]
    dataset = dataset.cf.drop_vars(drop_v)

    # Variable name standardization
    logger.debug(f"Renaming var '{VARIABLE_NAME}' to '{config.TCO3_VAR}'")
    dataset = dataset.cf.rename({VARIABLE_NAME: config.TCO3_VAR})
    dataset[config.TCO3_VAR].attrs.update(
        {"standard_name": config.TCO3_STANDARD_NAME, "units": "DU"}
    )

    # Coordinates name standardization
    logger.debug(f"Renaming coords '{dataset.coords}'")
    dataset = dataset.cf.rename({"latitude": "lat"})
    dataset = dataset.cf.rename({"longitude": "lon"})
    logger.debug(f"Adding standard_name to time coord")
    dataset.time.attrs["standard_name"] = "time"

    # Extend coordinates with axis
    logger.debug(f"Extending coords axis '[T,X,Y]'")
    dataset["time"].attrs["axis"] = "T"
    dataset["lon"].attrs["axis"] = "X"
    dataset["lat"].attrs["axis"] = "Y"

    # Deletion of not used coordinates
    logger.debug(f"Removing unused coords from '{list(dataset.coords)}'")
    dataset = dataset.squeeze(drop=True)
    keep_c = set(dataset.cf[c].name for c in ["X", "Y", "T"])
    drop_c = [v for v in dataset.coords if v not in keep_c]
    dataset = dataset.cf.drop_vars(drop_c)

    # Fill missing attributes
    dataset.attrs["Conventions"] = CONVENTIONS
    dataset.attrs["institution"] = INSTITUTION
    dataset.attrs["source"] = SOURCE

    # Return standard loaded tco3 dataset
    return dataset
