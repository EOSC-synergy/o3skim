"""Module in charge of dataset standardization when loading models."""
import logging


logger = logging.getLogger('o3skim.standardization')


def tco3(array, coord):
    """Standardizes a tco3 dataset.

    :param array: DataArray to standardize.
    :type array: xarray.DataArray

    :param coord: Coordinates map for tco3 variable. 
    :type coord: {'lon':str, 'lat':str, 'time':str}

    :return: Standardized DataArray.
    :rtype: xarray.DataArray 
    """
    array.name = 'tco3_zm'
    array = squeeze(array)
    array = rename_coords_tco3(array, **coord)
    array = sort(array)
    return array


def rename_coords_tco3(array, time, lat, lon):
    """Renames a tco3 array variable and coordinates"""
    logger.debug("Renaming '{0}' coordinates".format('tco3_zm'))
    return array.rename({time: 'time', lat: 'lat', lon: 'lon'})


def vmro3(array, coord):
    """Standardizes a vmro3 dataset.

    :param array: DataArray to standardize.
    :type array: xarray.DataArray

    :param coord: Coordinates map for vmro3 variable. 
    :type coord: {'lon':str, 'lat':str, 'plev':str, 'time':str}

    :return: Standardized DataArray.
    :rtype: xarray.DataArray 
    """
    array.name = 'vmro3_zm'
    array = squeeze(array)
    array = rename_coords_vmro3(array, **coord)
    array = sort(array)
    return array


def rename_coords_vmro3(array, time, plev, lat, lon):
    """Renames a vmro3 array variable and coordinates"""
    logger.debug("Renaming '{0}' coordinates".format('vmro3_zm'))
    return array.rename({time: 'time', plev: 'plev', lat: 'lat', lon: 'lon'})


def squeeze(array):
    """Squeezes the 1-size dimensions on an array"""
    logger.debug("Squeezing coordinates in dataset")
    return array.squeeze(drop=True)


def sort(array):
    """Sorts an array by coordinates"""
    logger.debug("Sorting coordinates in dataset")
    return array.sortby(list(array.coords))
