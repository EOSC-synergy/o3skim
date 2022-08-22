import glob
import logging

import numpy as np
import pandas as pd
import xarray as xr
from o3skim import utils
from o3skim.settings import TCO3_DATA_VARIABLE as DATA_VARIABLE
from o3skim.settings import TCO3_STANDARD_NAME as STANDARD_NAME
from o3skim.settings import TCO3_STANDARD_UNIT as STANDARD_UNIT
from o3skim.settings import TCO3_UNITS_CONVERSION as CONVERSION

## Application logger
logger = logging.getLogger(__name__)


DELIMITER = "\s+"  # Delimiter character for row values on the table
LOADING_UNITS = "DU"

def load_tco3(model_path):
    """Loads and returns a SBUV DataArray model and the dataset
    attributes. Note SBUV models do not have longitude coordinate.
    :param model_path: Paths expression to the dataset text file
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading SBUV GSFC data from: %s", model_path)
    textfile = glob.glob(model_path)
    if len(textfile) == 1:
        textfile = textfile[0]
    else:
        raise ValueError(f"Only 1 text file supported '{textfile}'")

    # Open textfile as tables using chunkio utility
    logger.debug(f"Opening textfile {textfile} as strio")
    with open(textfile, "r") as strio:
        tables = utils.chunkio("SBUV", strio)

    # Read tables as dataArrays and concatenate them
    logger.debug(f"Extracting dataArrays from textfile")
    arrays = []
    for head, chunk in tables:
        header = head[0:-2].split(" ")  # Split head strings
        year = int(header[0])  # First value in header is the year
        table = pd.read_table(chunk, sep=DELIMITER, index_col=[0, 1], dtype="float32")
        lat = np.float32([(l1 + l2) / 2 for l1, l2 in table.index])
        time = [pd.datetime(year, m, 1) for m in range(1, 13)]
        array = xr.DataArray(table, dict(lat=lat, time=time), ["lat", "time"])
        array.values.flat[array.values.flat == 0.0] = np.nan
        arrays.append(array)

    # Generate dataset from dataArray
    logger.debug(f"Generating dataset from dataArray")
    ozone = xr.concat(arrays, "time").expand_dims(dim="lon", axis=0)
    dataset = xr.Dataset(
        data_vars={
            DATA_VARIABLE: xr.Variable(
                *[ozone.dims, ozone.values/CONVERSION[LOADING_UNITS]],
                attrs=dict(
                    standard_name=STANDARD_NAME,
                    long_name="Total column of ozone in the atmosphere",
                    units=STANDARD_UNIT,
                ),
            ),
            "lon_bnds": xr.Variable(["lon", "bnds"], [(0, 360)]),
            "lat_bnds": xr.Variable(["lat", "bnds"], table.index.to_list()),
        },
        coords={
            "lon": xr.Variable(
                *[["lon"], np.float32([0])],
                attrs=dict(
                    standard_name="longitude",
                    axis="X",
                    units="degrees_east",
                    long_name="Longitude of the grid center",
                    bounds="lon_bnds",
                ),
            ),
            "lat": xr.Variable(
                *[["lat"], lat],
                attrs=dict(
                    standard_name="latitude",
                    axis="Y",
                    units="degrees_north",
                    long_name="Latitude of the grid center",
                    bounds="lat_bnds",
                ),
            ),
            "time": xr.Variable(
                *[["time"], ozone.time],
                attrs=dict(
                    standard_name="time",
                    axis="T",
                    long_name="time",
                ),
            ),
        },
        attrs=dict(
            Conventions="CF-1.8",
            title="SBUV Merged Ozone Data Set (MOD)",
            institution="NASA Goddard Space Flight Center, Greenbelt, MD 20771",
            source="https://acd-ext.gsfc.nasa.gov",
            comment="Text file parsed and extended to follow CF conventions",
        ),
    )

    return dataset
