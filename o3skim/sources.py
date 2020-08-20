"""This module creates the sources objects"""
import glob
import yaml
import xarray as xr


def load(yaml_file):
    """Loads the .yaml file with the sources configurations"""
    with open(yaml_file, "r") as ymlfile:
        return yaml.load(ymlfile)


class Source:
    """Standarized datasets and methods from a data source"""
    def __init__(self, collections):
        self.model = {}
        for name, variables in collections.items():
            self.model[name] = Model(variables)


def get_tco3_zm(tco3_zm=None, **kwarg):
    """Gets and standarises the tco3_zm data"""
    if tco3_zm:
        fnames = glob.glob(tco3_zm['dir'] + "/*.nc")
        with xr.open_mfdataset(fnames) as ds:
            tco3_zm = ds.rename({
                tco3_zm['name']: 'tco3_zm',
                tco3_zm['coordinades']['time']: 'time',
                tco3_zm['coordinades']['lat']: 'lat',
                tco3_zm['coordinades']['lon']: 'lon'
            })['tco3_zm']
    return tco3_zm


def get_vrm_zm(vrm_zm=None, **kwarg):
    """Gets and standarises the vrm_zm data"""
    if vrm_zm:
        fnames = glob.glob(vrm_zm['dir'] + "/*.nc")
        with xr.open_mfdataset(fnames) as ds:
            vrm_zm = ds.rename({
                vrm_zm['name']: 'tco3_zm',
                vrm_zm['coordinades']['time']: 'time',
                vrm_zm['coordinades']['lat']: 'lat',
                vrm_zm['coordinades']['lon']: 'lon'
            })['tco3_zm']
    return vrm_zm


class Model:
    """Standarised model with standarised variables"""
    def __init__(self, variables):
        self.tco3_zm = get_tco3_zm(**variables)
        self.vrm_zm = get_vrm_zm(**variables)

