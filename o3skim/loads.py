"""Module in charge of model data loading."""
import glob
import logging

import numpy as np
import pandas as pd
import xarray as xr

from o3skim import utils

logger = logging.getLogger("o3skim.loads")


## ------------------------------------------------------------------
## CCMI-1 Load function ---------------------------------------------
def ccmi(
    model_path,
    variable_name="equivalent_thickness_at_stp_of_atmosphere_ozone_content",
    original_attributes=False,
):
    """Loads and returns a CCMI-1 DataArray model and the dataset
    attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :param variable_name: Variable to load from the dataset
    :param original_attributes: Flag to keep non CF standard attributes
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading CCMI-1 data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Clean of non cf attributes
    if not original_attributes:
        utils.cf_clean(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Variable '{variable_name}' loading")
    bounds = [dataset[v].attrs.get("bounds", None) for v in dataset.coords]
    bounds = [bound for bound in bounds if bound is not None]
    keep_v = set([dataset.cf[variable_name].name] + bounds)
    drop_v = [v for v in dataset.data_vars if v not in keep_v]
    dataset = dataset.cf.drop_vars(drop_v)

    # Variable name standardization
    logger.debug(f"Renaming var '{variable_name}' to 'tco3'")
    dataset = dataset.cf.rename({variable_name: "tco3"})

    # Deletion of not used coordinates
    logger.debug(f"Removing unused coords from '{dataset.coords}'")
    dataset = dataset.squeeze(drop=True)
    keep_c = set(dataset.cf[c].name for c in ["X", "Y", "T"])
    drop_c = [v for v in dataset.coords if v not in keep_c]
    dataset = dataset.cf.drop_vars(drop_c)

    # Load cftime variables to support mean operations
    # See https://github.com/NCAR/esmlab/issues/161
    logger.debug(f"Loading time variable '{dataset.cf}[time].load()'")
    dataset.cf["time"].load()
    if "bounds" in dataset.cf["time"].attrs:
        dataset[dataset.cf["time"].attrs["bounds"]].load()

    # Processing of skimming operations
    return dataset


## ------------------------------------------------------------------
## ECMWF Load function ----------------------------------------------
def ecmwf(
    model_path,
    variable_name="tco3",
    original_attributes=False,
):
    """Loads and returns a ECMWF DataArray model and the dataset
    attributes.
    :param model_path: Paths expression to the dataset netCDF files
    :param variable_name: Variable to load from the dataset
    :param original_attributes: Flag to keep non CF standard attributes
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading ECMWF data from: %s", model_path)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Complete coordinate attributes
    logger.debug("Completing dataset coordinate")
    dataset.longitude.attrs["standard_name"] = "longitude"
    dataset.latitude.attrs["standard_name"] = "latitude"
    dataset.time.attrs["standard_name"] = "time"

    # Clean of non cf attributes
    if not original_attributes:
        utils.cf_clean(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Variable '{variable_name}' loading")
    bounds = [dataset[v].attrs.get("bounds", None) for v in dataset.coords]
    bounds = [bound for bound in bounds if bound is not None]
    keep_v = set([dataset.cf[variable_name].name] + bounds)
    drop_v = [v for v in dataset.data_vars if v not in keep_v]
    dataset = dataset.cf.drop_vars(drop_v)

    # Variable name standardization
    logger.debug(f"Renaming var '{variable_name}' to 'tco3'")
    dataset = dataset.cf.rename({variable_name: "tco3"})

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
    logger.debug(f"Removing unused coords from '{dataset.coords}'")
    dataset = dataset.squeeze(drop=True)
    keep_c = set(dataset.cf[c].name for c in ["X", "Y", "T"])
    drop_c = [v for v in dataset.coords if v not in keep_c]
    dataset = dataset.cf.drop_vars(drop_c)

    # Load cftime variables to support mean operations
    # See https://github.com/NCAR/esmlab/issues/161
    logger.debug(f"Loading time variable '{dataset.cf}[time].load()'")
    dataset.cf["time"].load()
    if "bounds" in dataset.cf["time"].attrs:
        dataset[dataset.cf["time"].attrs["bounds"]].load()

    # Fill missing attributes
    dataset.attrs["source"] = ""  # TODO: Add source
    dataset.attrs[
        "institution"
    ] = "European Centre for Medium-Range Weather Forecasts"

    # Processing of skimming operations
    return dataset


## ------------------------------------------------------------------
## ESACCI Load function ---------------------------------------------
def esacci(
    model_path,
    variable_name="atmosphere_mole_content_of_ozone",
    original_attributes=False,
    time_position=-2,
):
    """Loads and returns a ESACCI DataArray model and the dataset
    attributes. Note the name structure is composed by sections:
    For example: ESACCI-OZONE-L3S-TC-MERGED-DLR_1M-20010302-fv0100.
    Therefore is needed to indicate the position in the string
    for the dataset time (7 or -2 for the case above).
    :param model_path: Paths expression to the dataset netCDF files
    :param variable_name: Variable to load from the dataset
    :param original_attributes: Flag to keep non CF standard attributes
    :param time_position: Name position for the dataset time.
    :return: Standardized Dataset.
    """

    def pf(ds):
        fpath = ds.encoding["source"]
        fname = fpath.split("/")[-1]
        fdate = fname.split("-")[time_position]
        time = pd.to_datetime(fdate)
        return ds.expand_dims(time=[time])

    # Loading of DataArray and attributes
    logger.info("Loading ESACCI data from: %s", model_path)
    kwargs = dict(preprocess=pf)
    dataset = xr.open_mfdataset(model_path, **kwargs)

    # Complete time coordinate attributes
    logger.debug("Completing dataset time coordinate")
    dataset.time.attrs["standard_name"] = "time"
    dataset.time.attrs["long_name"] = "time"

    # Clean of non cf attributes
    if not original_attributes:
        utils.cf_clean(dataset)

    # Extraction of variable as dataset
    logger.debug(f"Variable '{variable_name}' loading")
    bounds = [dataset[v].attrs.get("bounds", None) for v in dataset.coords]
    bounds = [bound for bound in bounds if bound is not None]
    keep_v = set([dataset.cf[variable_name].name] + bounds)
    drop_v = [v for v in dataset.data_vars if v not in keep_v]
    dataset = dataset.cf.drop_vars(drop_v)

    # Variable name standardization
    logger.debug(f"Renaming var '{variable_name}' to 'tco3'")
    dataset = dataset.cf.rename({variable_name: "tco3"})

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
    logger.debug(f"Removing unused coords from '{dataset.coords}'")
    dataset = dataset.squeeze(drop=True)
    keep_c = set(dataset.cf[c].name for c in ["X", "Y", "T"])
    drop_c = [v for v in dataset.coords if v not in keep_c]
    dataset = dataset.cf.drop_vars(drop_c)

    # Load cftime variables to support mean operations
    # See https://github.com/NCAR/esmlab/issues/161
    logger.debug(f"Loading time variable '{dataset.cf}[time].load()'")
    dataset.cf["time"].load()
    if "bounds" in dataset.cf["time"].attrs:
        dataset[dataset.cf["time"].attrs["bounds"]].load()

    # Processing of skimming operations
    return dataset


## ------------------------------------------------------------------
## SBUV Load function -----------------------------------------------
def sbuv(model_path, delimiter="\s+"):
    """Loads and returns a SBUV DataArray model and the dataset
    attributes. Note SBUV models do not have longitude coordinate.
    :param model_path: Paths expression to the dataset text file
    :param delimiter: Delimiter character for row values on the table
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading SBUV data from: %s", model_path)
    textfile = glob.glob(model_path)
    if len(textfile) == 1:
        textfile = textfile[0]
    else:
        raise ValueError(f"Only 1 text file supported '{textfile}'")

    # Open textfile as tables using chunkio utility
    logger.debug(f"Opening textfile {textfile} as strio")
    with open(textfile, "r") as strio:
        tables = utils.chunkio("SBUV", strio)

    # Read tables as dataarrays and concatenate them
    logger.debug(f"Extracting dataarrays from textfile")
    arrays = []
    for head, chunk in tables:
        header = head[0:-2].split(" ")  # Split head strings
        year = int(header[0])  # First value in header is the year
        table = pd.read_table(chunk, sep=delimiter, index_col=[0, 1])
        lat = [(l1 + l2) / 2 for l1, l2 in table.index]
        time = [pd.datetime(year, m, 1) for m in range(1, 13)]
        array = xr.DataArray(table, dict(lat=lat, time=time), ["lat", "time"])
        array.values.flat[array.values.flat == 0.0] = np.nan
        arrays.append(array)

    # Generate dataset from dataarray
    logger.debug(f"Generating dataset from datarray")
    ozone = xr.concat(arrays, "time").expand_dims(dim="lon", axis=0)
    dataset = xr.Dataset(
        data_vars=dict(
            tco3=xr.Variable(
                *[ozone.dims, ozone.values],
                attrs=dict(
                    standard_name="atmosphere_mole_content_of_ozone",
                    units="DU",
                    long_name="Total column of ozone in the atmosphere",
                ),
            ),
            lon_bnds=xr.Variable(["lon", "bnds"], [(0, 360)]),
            lat_bnds=xr.Variable(["lat", "bnds"], table.index.to_list()),
        ),
        coords=dict(
            lon=xr.Variable(
                *[["lon"], [0]],
                attrs=dict(
                    standard_name="longitude",
                    axis="X",
                    units="degrees_east",
                    long_name="Longitude of the grid center",
                    bounds="lon_bnds",
                ),
            ),
            lat=xr.Variable(
                *[["lat"], lat],
                attrs=dict(
                    standard_name="latitude",
                    axis="Y",
                    units="degrees_north",
                    long_name="Latitude of the grid center",
                    bounds="lat_bnds",
                ),
            ),
            time=xr.Variable(
                *[["time"], ozone.time],
                attrs=dict(
                    standard_name="time",
                    axis="T",
                    long_name="time",
                ),
            ),
        ),
        attrs=dict(
            Conventions="CF-1.8",
            title="SBUV Merged Ozone Data Set (MOD)",
            institution="NASA Goddard Space Flight Center, Greenbelt, MD 20771",
            source="https://acd-ext.gsfc.nasa.gov",
            comment="Text file parsed and extended to follow CF conventions",
        ),
    )

    return dataset
