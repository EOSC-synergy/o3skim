"""This module offers some utils for code management."""
import io
import logging

import numpy as np

from o3skim import attributes

logger = logging.getLogger("o3skim.utils")


def complete_coords(dataset):
    """Completes coordinates with CF standard attributes
    :param dataset: Dataset to modify
    """
    if "time" in dataset.cf.coords:  # Complete time attributes
        name = dataset.cf["time"].name
        dataset[name].attrs["standard_name"] = "time"
        dataset[name].attrs["axis"] = "T"
    if "longitude" in dataset.cf.coords:  # Complete longitude attributes
        name = dataset.cf["longitude"].name
        dataset[name].attrs["standard_name"] = "longitude"
        dataset[name].attrs["axis"] = "X"
    if "latitude" in dataset.cf.coords:  # Complete latitude attributes
        name = dataset.cf["latitude"].name
        dataset[name].attrs["standard_name"] = "latitude"
        dataset[name].attrs["axis"] = "Y"
    if "air_pressure" in dataset.cf.coords:  # Complete level attributes
        name = dataset.cf["air_pressure"].name
        dataset[name].attrs["standard_name"] = "air_pressure"
        dataset[name].attrs["axis"] = "Z"


def drop_vars_except(dataset, variable):
    """Drops all dataset variables except the listed and relative.
    :param dataset: Dataset to modify
    :param variable: Variable to keep on the dataset
    """
    # Find the bound variables linked to the coordinates
    bounds = [dataset[v].attrs.get("bounds", None) for v in dataset.coords]
    bounds = [bound for bound in bounds if bound is not None]
    # Add variable to set of variables to keep
    keep_v = set([dataset.cf[variable].name] + bounds)
    drop_v = [v for v in dataset.data_vars if v not in keep_v]
    # Drop variables not used
    return dataset.cf.drop_vars(drop_v)


def drop_unused_coords(dataset, coords=["X", "Y", "Z", "T"]):
    """Deletion of non standard coordinates (lon, lat and time).
    :param dataset: Dataset to modify
    """
    # Squeeze to remove dimensions with only 1 value
    dataset = dataset.squeeze(drop=True)
    # Set the unexpected coordinates
    keep_c = set(dataset.cf[c].name for c in dataset.cf.coords if c in coords)
    drop_c = [v for v in dataset.coords if v not in keep_c]
    # Remove the non standard coordinates
    return dataset.cf.drop_vars(drop_c)


def delete_non_CFConvention_attributes(dataset):
    """Removes those existing attributes which are not in the CF specifications.
    :param dataset: Xarray dataset following CF conventions
    """
    # Clean global attributes
    cfds_attrs = set(attributes.global_attributes.index)
    dataset.attrs = {k: v for k, v in dataset.attrs.items() if k in cfds_attrs}
    # Clean coordinate attributes
    cfds_attrs = set(attributes.coordinate_attributes.index)
    for var in dataset.coords:
        var = dataset[var]
        var.attrs = {k: v for k, v in var.attrs.items() if k in cfds_attrs}
    # Clean data variables attributes
    cfds_attrs = set(attributes.variables_attributes.index)
    for var in dataset.data_vars:
        var = dataset[var]
        var.attrs = {k: v for k, v in var.attrs.items() if k in cfds_attrs}


def chunkio(headid, str_iter):
    """Chunks an iterable of strings. The text passed by str_iter is
    evaluated element by element (normally line by line). The elements
    are grouped/chunked by every element (line) which contains a
    "headid".

    :param headid: Line key word to separate chunks.
    :type headid: str

    :param str_iter: Iterable of strings to chunk.
    :type str_iter: iter

    :return: List of tuples with the header and chunk as StringIO.
    :rtype: [(str, :class:`io.StringIO`)]
    """
    heads = []
    chunks = []
    chunk = io.StringIO()
    for line in str_iter:
        if headid in line:
            heads.append(line)
            chunks.append(chunk)
            chunk.seek(0)  # rewind the stream
            chunk = io.StringIO()
        else:
            chunk.write(line)
    chunks.append(chunk)
    chunk.seek(0)  # rewind the stream
    return zip(heads, chunks[1:])
