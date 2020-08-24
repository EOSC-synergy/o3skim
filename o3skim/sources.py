"""This module creates the sources objects"""
import glob
import xarray as xr
import os.path
from . import utils


class Source:
    """Standarized datasets and methods from a data source"""

    def __init__(self, sname, collections):
        self._name = sname
        self._models = {}
        for name, variables in collections.items():
            self._models[name] = Model(variables)

    def skim(self):
        for name, model in self._models.items():
            path = self._name + "_" + name
            os.makedirs(path, exist_ok=True)
            model.skim(path)


class Model:
    """Standarised model with standarised variables"""

    def __init__(self, variables):
        self.__get_tco3_zm(**variables)
        self.__get_vrm_zm(**variables)

    def skim(self, path):
        if hasattr(self, '_tco3_zm'): 
            utils.to_netcdf(path, "tco3_zm", self._tco3_zm)
        if hasattr(self, '_vrm_zm'): 
            utils.to_netcdf(path, "vrm_zm", self._vrm_zm)

    def __get_tco3_zm(self, tco3_zm=None, **kwarg):
        """Gets and standarises the tco3_zm data"""
        if tco3_zm:
            fnames = glob.glob(tco3_zm['dir'] + "/*.nc")
            with xr.open_mfdataset(fnames) as ds:
                self._tco3_zm = ds.rename({
                    tco3_zm['name']: 'tco3_zm',
                    tco3_zm['coordinades']['time']: 'time',
                    tco3_zm['coordinades']['lat']: 'lat',
                    tco3_zm['coordinades']['lon']: 'lon'
                })['tco3_zm'].to_dataset()

    def __get_vrm_zm(self, vrm_zm=None, **kwarg):
        """Gets and standarises the vrm_zm data"""
        if vrm_zm:
            fnames = glob.glob(vrm_zm['dir'] + "/*.nc")
            with xr.open_mfdataset(fnames) as ds:
                self._vrm_zm = ds.rename({
                    vrm_zm['name']: 'tco3_zm',
                    vrm_zm['coordinades']['time']: 'time',
                    vrm_zm['coordinades']['lat']: 'lat',
                    vrm_zm['coordinades']['lon']: 'lon'
                })['tco3_zm'].to_dataset()


