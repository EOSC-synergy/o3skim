"""Module in charge of model data loading."""
import pandas as pd
import numpy as np
import logging
import xarray as xr
import o3skim.utils as utils


logger = logging.getLogger("o3skim.measures_sbuv")


def sbuv_function(variable_name, delimiter, textfile, **kwargs):
    """Returns an standardized dataset from a SBUV model.

    :return: Standardized DataSet.
    :rtype: :class:`iris.Cube`
    """
    datarray = sbuv(textfile[0], delimiter)
    dataset = datarray.to_dataset(name=variable_name)
    return dataset.assign_coords(lon=["nan"])


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
                version=header[3], name=header[1], description=" ".join(header[-3:])
            ),
            dims=["lat", "time"],
            coords=dict(
                lat=table.index, time=[pd.datetime(year, m, 1) for m in range(1, 13)]
            ),
        )
        array.values.flat[array.values.flat == 0.0] = np.nan
        arrays.append(array)
    return xr.concat(arrays, "time")
