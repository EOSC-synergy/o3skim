"""Module in charge of dataset normalization when loading models."""
import logging


logger = logging.getLogger('o3skim.normalization')


def run(datarray, variable, **coords):
    """Standardizes a DataArray.

    :return: Standardized DataArray.
    :rtype: :class:`xarray.DataArray`
    """
    logger.debug("Normalizing DataArray as %s", variable)
    datarray.name = variable
    datarray = _squeeze(datarray)
    datarray = _rename_coords(datarray, **coords)
    datarray = _sort(datarray)
    return datarray


def _rename_coords(array, **coords):
    """Renames an array variable and coordinates"""
    logger.debug("Renaming coordinates: {}".format(coords))
    for key, value in coords.items():
        try:
            array = array.rename({value: key})
        except ValueError:
            pass
    return array


def _squeeze(array):
    """Squeezes the 1-size dimensions on an array"""
    logger.debug("Squeezing coordinates in dataset")
    return array.squeeze(drop=True)


def _sort(array):
    """Sorts an array by coordinates"""
    logger.debug("Sorting coordinates in dataset")
    return array.sortby(list(array.coords))
