import logging

import xarray as xr
from o3skim import utils
from o3skim.settings import TCO3_DATA_VARIABLE as DATA_VARIABLE
from o3skim.settings import TCO3_STANDARD_NAME as STANDARD_NAME
from o3skim.settings import TCO3_STANDARD_UNIT as STANDARD_UNIT
from o3skim.settings import TCO3_UNITS_CONVERSION as CONVERSION

# Application logger
logger = logging.getLogger(__name__)

VARIABLE_NAME = "tco3"
INSTITUTION = "European Centre for Medium-Range Weather Forecasts"
SOURCE = ""  # TODO: Define source
LOAD_CHUNKS = {"time": "auto"}


def load_tco3(model_path):
    """Loads and returns a model and the dataset attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading model data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    kwargs["chunks"] = LOAD_CHUNKS
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Variable name standardization
    logger.debug(f"Renaming var '{VARIABLE_NAME}' to '{DATA_VARIABLE}'")
    dataset = dataset.cf.rename({VARIABLE_NAME: DATA_VARIABLE})
    dataset[DATA_VARIABLE].attrs.update({"standard_name": STANDARD_NAME})

    # Variable unit standardization
    logger.debug(f"Normalizing units to '{STANDARD_UNIT}'")
    dataset[DATA_VARIABLE] /= CONVERSION[dataset[DATA_VARIABLE].units]
    dataset[DATA_VARIABLE].attrs["units"] = STANDARD_UNIT
    dataset[DATA_VARIABLE] = dataset[DATA_VARIABLE].astype("float32")

    # Extraction of variable as dataset
    logger.debug(f"Removing all variable except '{DATA_VARIABLE}'")
    dataset = utils.drop_vars_except(dataset, DATA_VARIABLE)

    # Complete coordinate attributes
    logger.debug("Completing dataset coordinate")
    dataset = utils.normalize_coords(dataset)

    # Deletion of not used coordinates
    logger.debug(f"Removing unused coords from '{list(dataset.coords)}'")
    dataset = utils.drop_unused_coords(dataset)

    # Clean of non cf attributes
    logger.debug("Removing all non CF convention attributes")
    utils.delete_non_CFConvention_attributes(dataset)

    # Fill missing attributes
    dataset.attrs["institution"] = INSTITUTION
    dataset.attrs["source"] = SOURCE

    # Return standard loaded tco3 dataset
    return dataset
