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

from o3skim import utils
from o3skim import standardization


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

    def skim(self, groupby=None, **kwargs):
        """Request to skim all source data into the current folder

        :param groupby: How to group output (None, year, decade).
        :type groupby: str, optional
        """
        for name, model in self._models.items():
            dirname = self._name + "_" + name
            os.makedirs(dirname, exist_ok=True)
            logger.info("Skim data from '%s'", dirname)
            model.to_netcdf(dirname, groupby, **kwargs)


class Model(xr.Dataset):
    """Conceptual class for model with variables. It is produced by the 
    loading of the variables to be skimmed.

    :param variables: Dictionary with information about how to load
        the source where each 'key' is the name of the variable to 
        load and the value is the load details.
    :type variables: dict
    """

    def __init__(self, specifications):
        ds = xr.Dataset()
        for variable in specifications:
            load = standardization.load(variable, specifications[variable])
            ds = ds.merge(load)
        # Containment
        self.dataset = ds

    def __getattr__(self, attr):
        # Delegation (get)
        return getattr(self.dataset, attr)

    def __setattr__(self, attr, value):
        # Delegation (set)
        setattr(self.dataset, attr, value)

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
            return [("", self)]

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
            var_models.append((var, self[var].to_dataset()))
        return var_models

    def to_netcdf(self, path, delta=None, **kwargs):
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
                datasets.append(ds2)
                if t_range == "":
                    paths.append(path + "/" + var + ".nc")
                else:
                    paths.append(path + "/" + var + "_" + t_range + ".nc")

        logging.info("Save dataset into: %s", paths)
        if paths:
            xr.save_mfdataset(datasets, paths, **kwargs)
