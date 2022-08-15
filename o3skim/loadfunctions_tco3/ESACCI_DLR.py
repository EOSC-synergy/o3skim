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


def load_tco3(model_path):
    """Loads and returns a ESACCI DLR DataArray model and the dataset
    attributes. Note the name structure is composed by sections:
    For example: ESACCI-OZONE-L3S-TC-MERGED-DLR_1M-20010302-fv0100.
    :param model_path: Paths expression to the dataset netCDF files
    :return: Standardized Dataset.
    """

    def pf(dataset):
        if not "id" in dataset.attrs:
            raise ValueError("Unknown ESACCI dataset")
        if "ESACCI-OZONE-L3S-TC-MERGED-DLR_1M" in dataset.id:
            fpath = dataset.encoding["source"]
            fname = fpath.split("/")[-1]
            fdate = fname.split("-")[-2]
            time = pd.to_datetime(fdate)
            return dataset.expand_dims(time=[time])
        elif "C3S_OZONE-L4-TC-ASSIM_MSR" in dataset.id:
            dataset.attrs["Conventions"] = "CF-1.8"
            dataset.attrs["institution"] = dataset.Affiliation
            dataset.attrs["source"] = dataset.Data_created_by
            tco3 = dataset.total_ozone_column
            tco3.attrs["standard_name"] = "atmosphere_mole_content_of_ozone"
            tco3.attrs["units"] = "DU"
            return dataset

    # Loading of DataArray and attributes
    logger.info("Loading ESACCI data from: %s", model_path)
    kwargs = dict(preprocess=pf, chunks={"time": "auto"})
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Complete time coordinate attributes
    logger.debug("Completing dataset time coordinate")
    dataset.time.attrs["standard_name"] = "time"
    dataset.time.attrs["long_name"] = "time"

    # Clean of non cf attributes
    logger.debug(f"Removing all non CF convention attributes")
    utils.delete_non_CFConvention_attributes(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Removing all variable except '{VARIABLE_NAME}'")
    dataset = utils.drop_vars_except(dataset, VARIABLE_NAME)

    # Variable name standardization
    logger.debug(f"Renaming var '{VARIABLE_NAME}' to '{DATA_VARIABLE}'")
    dataset = dataset.cf.rename({VARIABLE_NAME: DATA_VARIABLE})
    dataset[DATA_VARIABLE].attrs.update(
        {"standard_name": STANDARD_NAME}
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
    dataset = utils.drop_unused_coords(dataset)

    # Convert dtype lon and lat to common float32 to reduce size
    logger.debug(f"Converting lat&lon coordinates to 'float32'")
    utils.float_to_float32(dataset, "lon")
    utils.float_to_float32(dataset, "lat")

    # Return standard loaded tco3 dataset
    return dataset
