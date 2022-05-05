"""Module in charge of model data loading."""
import logging

import numpy as np
import pandas as pd
import xarray as xr

from o3skim import utils

logger = logging.getLogger("o3skim.loads")


## ------------------------------------------------------------------
## CCMI-1 Load function ---------------------------------------------
def ccmi(
    model_paths,
    variable_name="equivalent_thickness_at_stp_of_atmosphere_ozone_content",
    original_attributes=False,
):
    """Loads and returns a CCMI-1 DataArray model and the dataset
    attributes.
    :param paths: Paths expression to the dataset netCDF files.
    :param variable: Variable to load from the dataset.
    :return: Standardized Dataset.
    """

    # Loading of DataArray and attributes
    logger.info("Loading CCMI-1 data from: %s", model_paths)
    kwargs = dict(data_vars="minimal", concat_dim="time", combine="nested")
    dataset = xr.open_mfdataset(model_paths, **kwargs)

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
    logger.debug(f"Renaming var '{variable_name}' to 'toz'")
    dataset = dataset.cf.rename({variable_name: "toz"})

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
def ecmwf(paths, variable):
    """Loads and returns a ECMWF DataArray model and the dataset
    attributes.
    :param paths: Paths expression to the dataset netCDF files.
    :param variable: Variable to load from the dataset.
    :return: Standardized DataArray.
    """
    logger.debug("Loading ECMWF data from: %s", paths)
    if len(paths) == 1:
        paths = paths[0]
    with xr.open_mfdataset(paths) as dataset:
        datarray = dataset[variable]
        ds_attrs = dataset.attrs
    return datarray, ds_attrs


## ------------------------------------------------------------------
## ESACCI Load function ---------------------------------------------
def esacci(variable, time_position, paths):
    """Loads and returns a ESACCI DataArray model and the dataset
    attributes. Note the name structure is composed by sections:
    For example: ESACCI-OZONE-L3S-TC-MERGED-DLR_1M-20010302-fv0100.
    Therefore is needed to indicate the position in the string
    for the dataset time (7 or -2 for the case above).

    :param variable: Variable to load from the dataset.
    :type variable: str

    :param time_position: Name position for the dataset time.
    :type time_position: int

    :param paths: Paths expression to the dataset netCDF files.
    :type paths: str or [str]

    :return: Standardized DataArray.
    :rtype: (:class:`xarray.DataArray`, dict)
    """
    if len(paths) == 1:
        paths = paths[0]

    def pf(ds):
        fpath = ds.encoding["source"]
        fname = fpath.split("/")[-1]
        fdate = fname.split("-")[time_position]
        time = pd.to_datetime(fdate)
        return ds.expand_dims(time=[time])

    with xr.open_mfdataset(paths, preprocess=pf) as dataset:
        datarray = dataset[variable]
        ds_attrs = dataset.attrs
    return datarray, ds_attrs


## ------------------------------------------------------------------
## SBUV Load function -----------------------------------------------
def sbuv(textfile, delimiter):
    """Loads and returns a SBUV DataArray model and the dataset
    attributes. Note SBUV models do not have longitude coordinate.

    :param textfile: Location to the textfile with model information.
    :type textfile: str

    :param delimiter: Delimiter character for row values on the table.
    :type delimiter: str or [str]

    :return: Standardized DataArray.
    :rtype: (:class:`xarray.DataArray`, {})
    """
    with open(textfile, "r") as strio:
        tables = utils.chunkio("SBUV", strio)
    arrays = []
    for head, chunk in tables:
        header = head[0:-2].split(" ")
        year = int(header[0])
        table = pd.read_table(chunk, sep=delimiter, index_col=[0, 1])
        table.index = [(int(l1) + int(l2)) / 2 for l1, l2 in table.index]
        array = xr.DataArray(
            data=table,
            attrs=dict(
                version=header[3],
                name=header[1],
                description=" ".join(header[-3:]),
            ),
            dims=["lat", "time"],
            coords=dict(
                lat=table.index,
                time=[pd.datetime(year, m, 1) for m in range(1, 13)],
            ),
        )
        array.values.flat[array.values.flat == 0.0] = np.nan
        arrays.append(array)
    return xr.concat(arrays, "time"), {}
