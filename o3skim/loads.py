"""
Module in charge of data loading and standardization.
"""
import logging

from o3skim import standardization
from o3skim import utils
import xarray as xr


logger = logging.getLogger('load')


def tco3(name, paths, coordinates, metadata={}):
    """Function to load data as standardized tco3_zm.

    :param name: Variable to retrieve after loading datasets.
    :type name: str

    :param paths: Regex expresion with paths to the datasets to load.
    :type paths: str

    :param coordinates: Coordinates map translation from original datasets.
    :type coordinates: dict

    :param metadata: Variable specific metadata. 
    :type metadata: dict, optional

    :return: Tuple with standardized tco3 data array, original dataset
        attributes and variable specific metadata.
    :rtype: tuple (:class:`xarray.DataArray`, dict, dict)
    """
    logger.debug("Loading tco3 data from: %s", paths)
    with xr.open_mfdataset(paths) as dataset:
        datarray = standardization.tco3(
            array=dataset[name],
            coord=coordinates)
        ds_attrs = dataset.attrs
    return datarray, ds_attrs, metadata


def vmro3(name, paths, coordinates, metadata={}):
    """Function to load data as standardized vmro3_zm.

    :param name: Variable to retrieve after loading datasets.
    :type name: str

    :param paths: Regex expresion with paths to the datasets to load.
    :type paths: str

    :param coordinates: Coordinates map translation from original datasets.
    :type coordinates: dict

    :param metadata: Variable specific metadata. 
    :type metadata: dict, optional

    :return: Tuple with standardized vmro3 data array, original dataset
        attributes and variable specific metadata.
    :rtype: tuple (:class:`xarray.DataArray`, dict, dict)
    """
    logger.debug("Loading vmro3 data from: %s", paths)
    with xr.open_mfdataset(paths) as dataset:
        datarray = standardization.vmro3(
            array=dataset[name],
            coord=coordinates)
        ds_attrs = dataset.attrs
    return datarray, ds_attrs, metadata
