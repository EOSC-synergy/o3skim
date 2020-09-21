"""This module creates the sources objects"""
import glob
import xarray as xr
import os.path
import logging
from . import utils

logger = logging.getLogger('o3skim.sources')


class Source:
    """Standarized datasets and methods from a data source"""

    def __init__(self, sname, collections):
        self._name = sname
        self._models = {}
        logging.info("Load source '%s'", self._name)
        for name, variables in collections.items():
            logging.info("Load model '%s'", name)
            self._models[name] = Model(variables)

    def skim(self):
        for name, model in self._models.items():
            path = self._name + "_" + name
            os.makedirs(path, exist_ok=True)
            logger.info("Skim data from '%s'", path)
            model.skim(path)


class Model:
    """Standarised model with standarised variables"""

    def __init__(self, variables):
        if 'tco3_zm' in variables:
            logger.debug("Load 'tco3_zm' data")
            self.__get_tco3_zm(**variables)
        if 'vrm_zm' in variables:
            logger.debug("Load 'vrm_zm' data")
            self.__get_vrm_zm(**variables)

    def skim(self, path):
        if hasattr(self, '_tco3_zm'):
            logger.debug("Skim 'tco3_zm' data")
            utils.to_netcdf(path, "tco3_zm", self._tco3_zm)
        if hasattr(self, '_vrm_zm'):
            logger.debug("Skim 'vrm_zm' data")
            utils.to_netcdf(path, "vrm_zm", self._vrm_zm)

    def __get_tco3_zm(self, tco3_zm, **kwarg):
        """Gets and standarises the tco3_zm data"""
        fnames = glob.glob(tco3_zm['dir'] + "/*.nc")
        with xr.open_mfdataset(fnames) as dataset:
            dataset = dataset.rename({
                tco3_zm['name']: 'tco3_zm',
                tco3_zm['coordinades']['time']: 'time',
                tco3_zm['coordinades']['lat']: 'lat',
                tco3_zm['coordinades']['lon']: 'lon'
            })['tco3_zm'].to_dataset()
            self._tco3_zm = dataset.mean(dim='lon')

    def __get_vrm_zm(self, vrm_zm, **kwarg):
        """Gets and standarises the vrm_zm data"""
        fnames = glob.glob(vrm_zm['dir'] + "/*.nc")
        with xr.open_mfdataset(fnames) as dataset:
            dataset = dataset.rename({
                vrm_zm['name']: 'vrm_zm',
                vrm_zm['coordinades']['time']: 'time',
                vrm_zm['coordinades']['plev']: 'plev',
                vrm_zm['coordinades']['lat']: 'lat',
                vrm_zm['coordinades']['lon']: 'lon'
            })['vrm_zm'].to_dataset()
            self._vrm_zm = dataset.mean(dim='lon')
