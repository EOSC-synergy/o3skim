"""Module in charge of dataset standardization when loading models."""
import logging
import o3skim.loads as loads
import o3skim.normalization as normalization

logger = logging.getLogger('o3skim.standardization')


def ccmi_function(parameter, variable, paths, **coords):
    datarray, attrs = loads.ccmi(variable[0], paths)
    datarray = normalization.run(datarray, parameter[0], **coords)
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    return dataset


def ecmwf_function(parameter, variable, paths, **coords):
    datarray, attrs = loads.ecmwf(variable[0], paths)
    datarray = normalization.run(datarray, parameter[0], **coords)
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    return dataset


def esacci_function(parameter, variable, time_position, paths, **coords):
    datarray, attrs = loads.esacci(variable[0], time_position, paths)
    datarray = normalization.run(datarray, parameter[0], **coords)
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    return dataset


def sbuv_function(parameter, delimiter, textfile):
    datarray, attrs = loads.sbuv(textfile[0], delimiter)
    datarray = normalization.run(datarray, parameter[0])
    dataset = datarray.to_dataset(name=parameter[0])
    dataset.attrs = attrs
    if parameter[0] == 'tco3_zm':
        return dataset.assign_coords(lon=['nan'])
    if parameter[0] == 'vmro3_zm':
        raise NotImplementedError("Load of vmro3 not available")
