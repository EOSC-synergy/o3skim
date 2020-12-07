"""Module in charge of dataset standardization when loading models."""

import logging
import xarray as xr
from o3skim import utils

logger = logging.getLogger('o3skim.standardization')

# tco3 standardization
tco3_standard_name = 'tco3_zm'
tco3_mean_coordinate = 'lon'
tco3_standard_coordinates = [
    'time',
    'lat',
    'lon'
]

# vmro3 standardization
vmro3_standard_name = 'vmro3_zm'
vmro3_mean_coordinate = 'lon'
vmro3_standard_coordinates = [
    'time',
    'plev',
    'lat',
    'lon'
]


@utils.return_on_failure("Error when loading '{0}'".format(tco3_standard_name),
                         xr.Dataset())
def __load_tco3(name, paths, coordinates):
    """Loads and standarises the tco3 data"""
    logger.debug("Standard loading of '{0}' data".format(tco3_standard_name))
    with xr.open_mfdataset(paths) as dataset:
        dataset = dataset.rename({
            **{name: tco3_standard_name},
            **{coordinates[x]: x for x in tco3_standard_coordinates}
        })[tco3_standard_name].to_dataset()
        return dataset.mean(dim=tco3_mean_coordinate)


@utils.return_on_failure("Error when loading '{0}'".format(vmro3_standard_name),
                         xr.Dataset())
def __load_vmro3(name, paths, coordinates):
    """Loads and standarises the vmro3 data"""
    logger.debug("Standard loading of '{0}' data".format(vmro3_standard_name))
    with xr.open_mfdataset(paths) as dataset:
        dataset = dataset.rename({
            **{name: vmro3_standard_name},
            **{coordinates[x]: x for x in vmro3_standard_coordinates}
        })[vmro3_standard_name].to_dataset()
        return dataset.mean(dim=vmro3_mean_coordinate)


# Load case dictionary
__loads = {
    tco3_standard_name: __load_tco3,
    vmro3_standard_name: __load_vmro3
}


# Non existing variable exception
class UnknownVariable(Exception):
    """To raise if variable to treat is unknown"""

    def __init__(self, variable, message="Unknown variable"):
        self.variable = variable
        self.message = message
        super().__init__(self.message)


def load(variable, configuration):
    """Loads and standarises the variable using a specific 
       configuration.
    
    :param variable: Loadable variable.
    :type variable: str

    :param configuration: Configuration to apply standardization.
    :type configuration: dict

    :return: A list of tuples (range, group model). 
    :rtype: [(str, Model)]    
    """
    try:
        function = __loads[variable]
    except KeyError:
        raise UnknownVariable(variable)
    return function(**configuration)
