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
import datetime
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
            model.to_netcdf(dirname, groupby)


xr.Dataset.__init__

class Model(xr.Dataset):
    """Conceptual class for model with variables. It is produced by the 
    loading of the variables to be skimmed.

    :param variables: Dictionary with information about how to load
        the source where each 'key' is the name of the variable to 
        load and the value is the load details.
    :type variables: dict
    """

    def __init__(self, variables):
        ds = xr.Dataset()
        if 'tco3_zm' in variables:
            logger.debug("Load 'tco3_zm' data")
            ds = ds.merge(get_tco3_zm(**variables))
        if 'vmro3_zm' in variables:
            logger.debug("Load 'vmro3_zm' data")
            ds = ds.merge(get_vmro3_zm(**variables))
        # Containment
        self.dataset = ds

    def __getattr__(self,attr):
        # Delegation
        return getattr(self.dataset, attr)

    def groupby(self, delta='year'):
        """Returns a GroupBy object for performing grouped operations
           over the time coordinate.

        A groupby operation involves some combination of splitting 
        the object, applying a function, and combining the results.

        :param delta: How to group files (None, year, decade).
        :type delta: str or None, optional

        :return: A list of tuples (range, group model). 
        :rtype: [(str, Model)] 
        """

        if delta == None:
            return "", self

        logger.debug("Group model by: '{0}' ".format(delta))
        if delta == 'year':
            delta = 1
        if delta == 'decade':
            delta = 10

        years = self.indexes['time'].map(lambda x: x.year // delta * delta)
        group = super().groupby(xr.DataArray(years))

        return [(str(y) + "-" + str(y + delta), ds) for y, ds in group]

    def split_variables(self):
        """Request to split model variables into individual models. 

        :return: A list of tuples (variable, var Model). 
        :rtype: [(str, Model)]
        """
        var_models = []
        for var in self.data_vars:
            logger.debug("Internal var: '{0}' to dataset".format(var))
            var_models.extend((var, self[var].to_dataset()))
        return var_models

    def to_netcdf(self, path, *arg, delta=None, **kwargs):
        """Request to save model data into the specified path

        :param path: Path where to place the output files.
        :type path: str

        :param delta: How to group output (None, year, decade).
        :type delta: str or None, optional

        For extra inputs see also
        -------------------------
        xarray.save_mfdataset
        """
        datasets = []
        paths = []
        for t_range, ds1 in self.groupby(delta=delta):
            for var, ds2 in ds1.split_variables():
                datasets.extend(ds2)
                if t_range == "":
                    paths.extend(path + "/" + var + ".nc")
                else:
                    paths.extend(path + "/" + var + "_" + t_range + ".nc")

        logging.info("Save dataset into: %s", paths)
        xr.save_mfdataset(datasets, paths, *arg, **kwargs)


@utils.return_on_failure("Error when loading 'tco3_zm'")
def get_tco3_zm(tco3_zm, **kwarg):
    """Gets and standarises the tco3_zm data"""
    with xr.open_mfdataset(tco3_zm['paths']) as dataset:
        dataset = dataset.rename({
            tco3_zm['name']: 'tco3_zm',
            tco3_zm['coordinates']['time']: 'time',
            tco3_zm['coordinates']['lat']: 'lat',
            tco3_zm['coordinates']['lon']: 'lon'
        })['tco3_zm'].to_dataset()
        return dataset.mean(dim='lon')


@utils.return_on_failure("Error when loading 'vmro3_zm'")
def get_vmro3_zm(vmro3_zm, **kwarg):
    """Gets and standarises the vmro3_zm data"""
    with xr.open_mfdataset(vmro3_zm['paths']) as dataset:
        dataset = dataset.rename({
            vmro3_zm['name']: 'vmro3_zm',
            vmro3_zm['coordinates']['time']: 'time',
            vmro3_zm['coordinates']['plev']: 'plev',
            vmro3_zm['coordinates']['lat']: 'lat',
            vmro3_zm['coordinates']['lon']: 'lon'
        })['vmro3_zm'].to_dataset()
        return dataset.mean(dim='lon')
