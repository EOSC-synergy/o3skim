"""Module in charge of creating the sources objects.
This objects are responsible of loading and the netCDF
files from data and do the standardization during the
process.

After the data are loaded and the instances created, 
it is possible to use the internal methods to produce
the desired output.
"""

import glob
import xarray as xr
import os.path
import logging
from . import utils

logger = logging.getLogger('o3skim.sources')


class Source:
    """Conceptual class for a data source. It is produced by the loading 
    and generation of internal instances from each data source model.

    :param sname: Name to provide to the source. The folder name with the 
        skimmed output data is preceded with this name before '_'.
    :type sname: str
    
    :param collections: Dictionary where each 'key' is a name and its 
        value another dictionary with the variables contained at this
        model. See :class:`o3skim.sources.Model` for further details.
    :type collections: dict
    """

    def __init__(self, sname, collections):
        self._name = sname
        self._models = {}
        logging.info("Load source '%s'", self._name)
        for name, variables in collections.items():
            logging.info("Load model '%s'", name)
            self._models[name] = Model(variables)

    def skim(self, groupby=None):
        """Request to skim all source data into the current folder

        :param groupby: How to group output (None, year, decade).
        :type groupby: str, optional
        """
        for name, model in self._models.items():
            dirname = self._name + "_" + name
            os.makedirs(dirname, exist_ok=True)
            logger.info("Skim data from '%s'", dirname)
            model.skim(dirname, groupby)


class Model:
    """Conceptual class for model with variables. It is produced by the 
    loading of the variables to be skimmed.

    :param variables: Dictionary with information about how to load
        the source where each 'key' is the name of the variable to 
        load and the value is the load details.
    :type variables: dict
    """

    def __init__(self, variables):
        if 'tco3_zm' in variables:
            logger.debug("Load 'tco3_zm' data")
            self.__get_tco3_zm(**variables)
        if 'vmro3_zm' in variables:
            logger.debug("Load 'vmro3_zm' data")
            self.__get_vmro3_zm(**variables)

    def skim(self, dirname, groupby=None):
        """Request to skim all source data into the specified path

        :param dirname: Path where to place the output files.
        :type dirname: str
        
        :param groupby: How to group output (None, year, decade).
        :type groupby: str, optional
        """
        if hasattr(self, '_tco3_zm'):
            logger.debug("Skim 'tco3_zm' data")
            utils.to_netcdf(dirname, "tco3_zm", self._tco3_zm, groupby)
        if hasattr(self, '_vmro3_zm'):
            logger.debug("Skim 'vmro3_zm' data")
            utils.to_netcdf(dirname, "vmro3_zm", self._vmro3_zm, groupby)

    @utils.return_on_failure("Error when loading 'tco3_zm'")
    def __get_tco3_zm(self, tco3_zm, **kwarg):
        """Gets and standarises the tco3_zm data"""
        with xr.open_mfdataset(tco3_zm['paths']) as dataset:
            dataset = dataset.rename({
                tco3_zm['name']: 'tco3_zm',
                tco3_zm['coordinates']['time']: 'time',
                tco3_zm['coordinates']['lat']: 'lat',
                tco3_zm['coordinates']['lon']: 'lon'
            })['tco3_zm'].to_dataset()
            self._tco3_zm = dataset.mean(dim='lon')

    @utils.return_on_failure("Error when loading 'vmro3_zm'")
    def __get_vmro3_zm(self, vmro3_zm, **kwarg):
        """Gets and standarises the vmro3_zm data"""
        with xr.open_mfdataset(vmro3_zm['paths']) as dataset:
            dataset = dataset.rename({
                vmro3_zm['name']: 'vmro3_zm',
                vmro3_zm['coordinates']['time']: 'time',
                vmro3_zm['coordinates']['plev']: 'plev',
                vmro3_zm['coordinates']['lat']: 'lat',
                vmro3_zm['coordinates']['lon']: 'lon'
            })['vmro3_zm'].to_dataset()
            self._vmro3_zm = dataset.mean(dim='lon')
