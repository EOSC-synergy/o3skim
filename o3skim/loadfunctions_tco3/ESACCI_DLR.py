import logging

import xarray as xr
from o3skim import config, utils
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
    utils.delete_non_CFConvention_attributes(dataset)

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

    # Return standard loaded tco3 dataset
    return dataset
