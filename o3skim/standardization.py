"""Module in charge of dataset standardization when loading models."""
import logging


logger = logging.getLogger('o3skim.standardization')


def run(datarray, variable, **coords):
    """Standardizes a DataArray.

    :return: Standardized DataArray.
    :rtype: :class:`xarray.DataArray`
    """
    logger.debug("Standardizing DataArray as %s", variable)
    datarray = _squeeze(datarray)
    datarray.name = variable
    if variable == 'tco3_zm':
        datarray = _rename_coords_tco3(datarray, **coords)
    if variable == 'vmro3_zm':
        datarray = _rename_coords_vmro3(datarray, **coords)
    datarray = _sort(datarray)
    return datarray


def _rename_coords_tco3(array, lat, lon, time='time', **Not_used):
    """Renames a tco3 array variable and coordinates"""
    logger.debug("Renaming '{0}' coordinates".format('tco3_zm'))
    return array.rename({time: 'time', lat: 'lat', lon: 'lon'})


def _rename_coords_vmro3(array, lat, lon, plev, time='time', **Not_used):
    """Renames a vmro3 array variable and coordinates"""
    logger.debug("Renaming '{0}' coordinates".format('vmro3_zm'))
    return array.rename({time: 'time', plev: 'plev', lat: 'lat', lon: 'lon'})


def _squeeze(array):
    """Squeezes the 1-size dimensions on an array"""
    logger.debug("Squeezing coordinates in dataset")
    return array.squeeze(drop=True)


def _sort(array):
    """Sorts an array by coordinates"""
    logger.debug("Sorting coordinates in dataset")
    return array.sortby(list(array.coords))
