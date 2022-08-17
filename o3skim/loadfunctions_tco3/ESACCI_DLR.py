import logging

import xarray as xr
from o3skim import utils
from o3skim.settings import TCO3_DATA_VARIABLE as DATA_VARIABLE
from o3skim.settings import TCO3_STANDARD_NAME as STANDARD_NAME
from o3skim.settings import TCO3_STANDARD_UNIT as STANDARD_UNIT
from o3skim.settings import TCO3_UNITS_CONVERSION as CONVERSION
import pandas as pd


## Application logger
logger = logging.getLogger(__name__)

VARIABLE_NAME = "atmosphere_mole_content_of_ozone"
LOAD_CHUNKS = {"time": "auto"}


def pf(dataset):
    date = dataset.encoding["source"].split("-")[-2]
    return dataset.expand_dims(time=[pd.to_datetime(date)])


def load_tco3(model_path):
    """Loads and returns a model and the dataset attributes. Note the name
    structure is composed by sections:
    For example: ESACCI-OZONE-L3S-TC-MERGED-DLR_1M-20010302-fv0100.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading model data from: %s", model_path)
    kwargs = dict(preprocess=pf, chunks=LOAD_CHUNKS)
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Variable name standardization
    logger.debug(f"Renaming var '{VARIABLE_NAME}' to '{DATA_VARIABLE}'")
    dataset = dataset.cf.rename({VARIABLE_NAME: DATA_VARIABLE})
    dataset[DATA_VARIABLE].attrs["standard_name"] = STANDARD_NAME

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
    logger.debug(f"Removing all non CF convention attributes")
    utils.delete_non_CFConvention_attributes(dataset)

    # Return standard loaded tco3 dataset
    return dataset
