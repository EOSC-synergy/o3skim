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
        logger.debug("Changing directory: '%s'", newdir)
        yield
    finally:
        os.chdir(prevdir)
        logger.debug("Restoring directory: '%s'", prevdir)


def return_on_failure(message, default=None):
    """Decorator to do not break but log. Note that the error stack
    is printed as well to do not lose relevant information.

    :param message: Additional message to log when the function fails.
    :type message: str

    :param default: Value to return if fails.
    :type default: any or None, optional
    """
    def decorate(function):
        def applicator(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except:
                # Log error with stack using root (not utils)
                logging.error(message, exc_info=True)
                return default
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
        config = yaml.safe_load(ymlfile)
        logging.debug("Configuration data: %s", config)
        return config
