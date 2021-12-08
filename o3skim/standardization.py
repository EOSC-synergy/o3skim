"""Module in charge of dataset standardization when loading models."""
# TODO: Units conversion
# TODO: Standardize variable names

import logging
import o3skim.loads as loads
import o3skim.normalization as normalization

logger = logging.getLogger('o3skim.standardization')


def ccmi_function(parameter, variable, paths, **coords):
    """Returns an standardized dataset from a CCMI-1 model.

    :return: Standardized DataSet.
    :rtype: :class:`xarray.DataSet`
    """
    datarray, attrs = loads.ccmi(variable[0], paths)
    datarray = normalization.run(datarray, parameter[0], **coords)
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    return dataset


def ecmwf_function(parameter, variable, paths, **coords):
    """Returns an standardized dataset from a ECMWF model.

    :return: Standardized DataSet.
    :rtype: :class:`xarray.DataSet`
    """
    datarray, attrs = loads.ecmwf(variable[0], paths)
    datarray = normalization.run(datarray, parameter[0], **coords)
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    return dataset


def esacci_function(parameter, variable, time_position, paths, **coords):
    """Returns an standardized dataset from a ESACCI model.

    :return: Standardized DataSet.
    :rtype: :class:`xarray.DataSet`
    """
    datarray, attrs = loads.esacci(variable[0], time_position, paths)
    datarray = normalization.run(datarray, parameter[0], **coords)
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    return dataset


def sbuv_function(parameter, delimiter, textfile):
    """Returns an standardized dataset from a SBUV model.

    :return: Standardized DataSet.
    :rtype: :class:`xarray.DataSet`
    """
    datarray, attrs = loads.sbuv(textfile[0], delimiter)
    datarray = normalization.run(datarray, parameter[0])
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    if parameter[0] == 'tco3_zm':
        return dataset.assign_coords(lon=['nan'])
    if parameter[0] == 'vmro3_zm':
        raise NotImplementedError("Load of vmro3 not available")
