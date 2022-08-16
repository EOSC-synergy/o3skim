import logging

import xarray as xr
from o3skim import utils
from o3skim.settings import VMRO3_DATA_VARIABLE as DATA_VARIABLE
from o3skim.settings import VMRO3_STANDARD_NAME as STANDARD_NAME
from o3skim.settings import VMRO3_STANDARD_UNIT as STANDARD_UNIT
from o3skim.settings import VMRO3_UNITS_CONVERSION as CONVERSION

## Application logger
logger = logging.getLogger(__name__)

VARIABLE_NAME = "mole_fraction_of_ozone_in_air"
LOAD_CHUNKS = None


def load_zmo3(model_path):
    """Loads and returns a model and the dataset attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset
    """

    # Loading of DataArray and attributes
    logger.info("Loading model data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    kwargs["chunks"] = LOAD_CHUNKS
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Complete coordinate attributes
    logger.debug("Completing dataset coordinate")
    utils.complete_coords(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Removing all variable except '{VARIABLE_NAME}'")
    dataset = utils.drop_vars_except(dataset, VARIABLE_NAME)

    # Deletion of not used coordinates
    logger.debug(f"Removing unused coords from '{list(dataset.coords)}'")
    dataset = utils.drop_unused_coords(dataset)

    # Clean non cf attributes
    logger.debug(f"Removing all non CF convention attributes")
    utils.delete_non_CFConvention_attributes(dataset)

    # Variable name standardization
    logger.debug(f"Renaming var '{VARIABLE_NAME}' to '{DATA_VARIABLE}'")
    dataset = dataset.cf.rename({VARIABLE_NAME: DATA_VARIABLE})
    dataset[DATA_VARIABLE].attrs["standard_name"] = STANDARD_NAME

    # Variable unit standardization
    logger.debug(f"Normalizing units to '{STANDARD_UNIT}'")
    dataset[DATA_VARIABLE] /= CONVERSION[dataset[DATA_VARIABLE].units]
    dataset[DATA_VARIABLE].attrs["units"] = STANDARD_UNIT

    # Load cftime variables to support mean operations
    # See https://github.com/NCAR/esmlab/issues/161
    logger.debug(f"Loading time variable '{dataset.cf['time'].name}'")
    dataset.cf["time"].load()
    if "bounds" in dataset.cf["time"].attrs:
        dataset[dataset.cf["time"].attrs["bounds"]].load()

    # Convert cftime variables to support mean operations
    logger.debug(f"Converting time coordinate to '<M8[ns]'")
    dataset["time"] = dataset["time"].astype("<M8[ns]")

    # Convert dtype plev and lat to common float32 to reduce size
    logger.debug(f"Converting lat&plev coordinates to 'float32'")
    dataset["lat"] = dataset["lat"].astype("float32")
    dataset["plev"] = dataset["plev"].astype("float32")

    # Processing of skimming operations
    return dataset
