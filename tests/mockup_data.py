"""This modules creates mockup data for testing"""

import xarray as xr
import numpy as np
import netCDF4
import os.path
import datetime


base = datetime.datetime(2000, 1, 1)
indexes = {
    'time': [base + datetime.timedelta(days=i) for i in range(365)],
    'plev': [x for x in range(1, 1000, 100)],
    'lat':  [x for x in range(-90, 90, 10)],
    'lon':  [x for x in range(-180, 180, 20)]
}


def data_vars(coordinades):
    """Creates a mock n-array with coordinade values"""
    alias = tuple(coordinades.values())
    dim = tuple(len(indexes[c]) for c in coordinades)
    return alias, np.ones(dim),


def map_coord(coordinades):
    """Creates a mock array by coordinade"""
    return {alias: indexes[c] for c, alias in coordinades.items()}


def dataset(name, coordinades):
    """Creates a dataset acording to the global module indexes"""
    return xr.Dataset(
        {name: data_vars(coordinades)},
        coords=map_coord(coordinades)
    )


def create_empty_netCDF(fname):
    """Creates a new empty netCDF file"""
    root_grp = netCDF4.Dataset(fname, 'w', format='NETCDF4')
    root_grp.description = 'Example simulation data'
    root_grp.close()


def netcdf(path, name, coordinades, **kwarg):
    """Creates or appends data to a mock netcdf file"""
    ds = dataset(name, coordinades)
    months, dsx = zip(*ds.groupby("time.month"))
    fnames = [path + "/source_file_%s.nc" % m for m in months]
    [create_empty_netCDF(fn) for fn in fnames if not os.path.isfile(fn)]
    xr.save_mfdataset(dsx, fnames, mode='a')
