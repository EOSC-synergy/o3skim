import logging

import xarray as xr
from o3skim import config, utils

## Application logger
logger = logging.getLogger(__name__)


VARIABLE_NAME = "tco3"
INSTITUTION = "European Centre for Medium-Range Weather Forecasts"
SOURCE = ""  # TODO: Define source

def load_tco3(model_path):
    """Loads and returns a ECMWF ECMWF DataArray model and the dataset
    attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading ECMWF ECMWF data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    kwargs["chunks"] = {"time": "auto"}
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Complete coordinate attributes
    logger.debug("Completing dataset coordinate")
    dataset.longitude.attrs["standard_name"] = "longitude"
    dataset.latitude.attrs["standard_name"] = "latitude"
    dataset.time.attrs["standard_name"] = "time"

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
        {"standard_name": config.TCO3_STANDARD_NAME}
    )

    # Coordinates name standardization
    logger.debug(f"Renaming coords '{dataset.coords}'")
    dataset = dataset.cf.rename({"latitude": "lat"})
    dataset = dataset.cf.rename({"longitude": "lon"})

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

    # Normalize values to Dobson Units
    # See, https://sacs.aeronomie.be/info/dobson.php
    logger.debug("Converting source data units to 'DU")
    if dataset[config.TCO3_VAR].units == "kg m**-2":  # 2.1415x10-5 kg[O3]/m2
        dataset[config.TCO3_VAR] /= 2.1415e-05
        dataset[config.TCO3_VAR].attrs.update({'units': "DU"})
    else:
        raise ValueError(f"Unexpected {dataset[config.TCO3_VAR].units} unit")

    # Fill missing attributes
    dataset.attrs["institution"] = INSTITUTION
    dataset.attrs["source"] = SOURCE

    # Return standard loaded tco3 dataset
    return dataset
