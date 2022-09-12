"""This module offers some utils for code management."""
import io
import logging

from o3skim import attributes

logger = logging.getLogger("o3skim.utils")


def normalize_coords(dataset):
    """Completes coordinates with CF standard attributes
    :param dataset: Dataset to modify
    :return: Modified dataset
    """
    if "time" in dataset.cf.coords:
        dataset = normalize_coord_time(dataset)
    if "longitude" in dataset.cf.coords:
        dataset = normalize_coord_lon(dataset)
    if "latitude" in dataset.cf.coords:
        dataset = normalize_coord_lat(dataset)
    if "air_pressure" in dataset.cf.coords:
        dataset = normalize_coord_plev(dataset)
    return dataset


def normalize_coord_time(dataset, name="time"):
    """Normalizes time coordinate with CF standard values and attributes.
    :param dataset: Dataset to modify
    :param name: New name for coordinate, defaults to "time"
    :return: Modified dataset
    """
    old_name = dataset.cf["time"].name
    dataset = dataset.cf.rename({old_name: name})
    dataset[name] = dataset[name].astype("<M8[ns]")
    dataset[name].attrs["axis"] = "T"
    dataset[name].attrs["long_name"] = "time"
    dataset[name].attrs["standard_name"] = "time"
    return dataset


def normalize_coord_lon(dataset, name="lon"):
    """Normalizes longitude coordinate with CF standard values and attributes.
    :param dataset: Dataset to modify
    :param name: New name for coordinate, defaults to "lon"
    :return: Modified dataset
    """
    old_name = dataset.cf["longitude"].name
    dataset = dataset.cf.rename({old_name: name})
    dataset[name] = dataset[name].astype("float32")
    dataset[name].attrs["axis"] = "X"
    dataset[name].attrs["long_name"] = "longitude"
    dataset[name].attrs["standard_name"] = "longitude"
    if dataset[name].units == "degrees_east":
        pass  # Correct units
    elif dataset[name].units == "degrees_west":
        dataset[name] = 360.0 - dataset[name]
        dataset[name].attrs["units"] = "degrees_east"
    return dataset


def normalize_coord_lat(dataset, name="lat"):
    """Normalizes latitude coordinate with CF standard values and attributes.
    :param dataset: Dataset to modify
    :param name: New name for coordinate, defaults to "lat"
    :return: Modified dataset
    """
    old_name = dataset.cf["latitude"].name
    dataset = dataset.cf.rename({old_name: name})
    dataset[name] = dataset[name].astype("float32")
    dataset[name].attrs["axis"] = "Y"
    dataset[name].attrs["long_name"] = "latitude"
    dataset[name].attrs["standard_name"] = "latitude"
    if dataset[name].units == "degrees_north":
        pass  # Correct units
    elif dataset[name].units == "degrees_south":
        dataset[name] = -dataset[name]
        dataset[name].attrs["units"] = "degrees_north"
    return dataset


def normalize_coord_plev(dataset, name="plev"):
    """Normalizes pressure coordinate with CF standard values and attributes.
    :param dataset: Dataset to modify
    :param name: New name for coordinate, defaults to "plev"
    :return: Modified dataset
    """
    old_name = dataset.cf["air_pressure"].name
    dataset = dataset.cf.rename({old_name: name})
    dataset[name] = dataset[name].astype("float32")
    dataset[name].attrs["axis"] = "Z"
    dataset[name].attrs["long_name"] = "air_pressure"
    dataset[name].attrs["standard_name"] = "air_pressure"
    if dataset[name].units == "Pa":
        pass  # Correct units
    elif dataset[name].units == "millibars":
        dataset[name] = 100.0 * dataset[name]
        dataset[name].attrs["units"] = "Pa"
    elif dataset[name].units == "hPa":
        dataset[name] = 100.0 * dataset[name]
        dataset[name].attrs["units"] = "Pa"
    return dataset


def drop_vars_except(dataset, variable):
    """Drops all dataset variables except the listed and relative.
    :param dataset: Dataset to modify
    :param variable: Variable to keep on the dataset
    """
    # Bounds does not behave correctly with xarray~=2022.6.0
    for coordinate in dataset.coords:
        dataset[coordinate].attrs.pop('bounds', None)
    # Drop variables not used
    drop_v = [v for v in dataset.data_vars if v != variable]
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
    """Removes attributes that are not in the CF specifications.
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
