"""This module offers some utils for code management. For example
utils to change easily from directory or create netCDF files.

Although this module is not expected to be used out of the o3skim
package, some functions might be convenient when using the python 
shell.
"""

from contextlib import contextmanager
import os
import yaml
import netCDF4
import xarray as xr
import logging

logger = logging.getLogger('o3skim.utils')


@contextmanager
def cd(newdir):
    """Changes the directory inside a 'with' context. When the code
    reaches the end of the 'with' block or the code fails, the 
    previous folder is restored.

    :param newdir: Path folder where to change the working directory.
    :type newdir: str
    """
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        logger.debug("Temp dir change to: '%s'", newdir)
        yield
    finally:
        os.chdir(prevdir)
        logger.debug("Restore directory: '%s'", prevdir)


def return_on_failure(message):
    """Decorator to do not break but log. Note that the error stack
    is printed as well to do not lose relevant information.

    :param message: Additional message to log when the function fails.
    :type message: str
    """
    def decorate(function):
        def applicator(*args, **kwargs):
            try:
                function(*args, **kwargs)
            except:
                # Log error with stak using root (not utils)
                logging.error(message, exc_info=True)
        return applicator
    return decorate


def load(yaml_file):
    """Loads the .yaml file and returns a python dictionary with all
    the yaml keys and values. Note a yaml file can have key:values 
    sotored inside values, therefore the returned dictionary might 
    have dictionaries stored inside values. 

    :param yaml_file: Path pointing to the yaml configuration file.
    :type yaml_file: str

    :return: Dictionary with the yaml structure key:value.
    :rtype: dict
    """
    with open(yaml_file, "r") as ymlfile:
        config = yaml.load(ymlfile)
        logging.debug("Configuration data: %s", config)
        return config


def create_empty_netCDF(fname):
    """Creates a new empty netCDF file.

    :param fname: Name and path where to create the file.
    :type fname: str
    """
    root_grp = netCDF4.Dataset(fname, 'w', format='NETCDF4')
    root_grp.description = 'Example simulation data'
    root_grp.close()


def to_netcdf(dirname, name, dataset, groupby=None):
    """Creates or appends data to named netCDF files.

    :param path: Location where to find or create the netCDF files.
    :type path: str

    :param name: Name/Prefix for file/s where to store the data.
    :type name: str

    :param dataset: Dataset to write to the netCDF file.
    :type dataset: :class:`xarray.Dataset`

    :param groupby: How to group files (None, year, decade).
    :type groupby: str, optional
    """
    def split_by_year(dataset):
        """Splits a dataset by year"""
        years, dsx = zip(*dataset.groupby("time.year"))
        fnames = [dirname + "/" + name + "_%s.nc" % y for y in years]
        return fnames, dsx

    def split_by_decade(dataset):
        """Splits a dataset by decade"""
        decades = dataset.indexes["time"].year//10*10
        decades, dsx = zip(*dataset.groupby(xr.DataArray(decades)))
        fnames = [dirname + "/" + name + "_%s-%s.nc" % (d, d+10) for d in decades]
        return fnames, dsx

    def no_split(dataset):
        """Does not split a dataset"""
        dsx = (dataset,)
        fnames = [dirname + "/" + name + ".nc"]
        return fnames, dsx

    split_by = {
        "year": split_by_year,
        "decade": split_by_decade
    }
    fnames, dsx = split_by.get(groupby, no_split)(dataset)

    logging.info("Save dataset into: %s", fnames)
    [create_empty_netCDF(fn) for fn in fnames if not os.path.isfile(fn)]
    xr.save_mfdataset(dsx, fnames, mode='a')
