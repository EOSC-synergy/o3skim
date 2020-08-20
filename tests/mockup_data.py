"""This modules creates mockup data for testing"""

import xarray as xr
import numpy as np
import netCDF4
import os.path


start = {'time':  0, 'plev':    0, 'lat': -90, 'lon': -180}
end = {'time': 20, 'plev': 1000, 'lat': +90, 'lon': +180}
step = {'time':  1, 'plev':  100, 'lat':  10, 'lon':   10}
size = {'time': 20, 'plev':   10, 'lat':  18, 'lon':   36}


def data_vars(coordinades):
    """Creates a mock n-array with coordinade values"""
    alias = tuple(coordinades.values())
    dim = tuple(size[c] for c in coordinades)
    return alias, np.ones(dim),


def map_coord(coordinades):
    """Creates a mock array by coordinade"""
    return {alias: [x for x in range(start[c], end[c], step[c])]
            for c, alias in coordinades.items()}


def netcdf(fname, name, coordinades, **kwarg):
    """Creates or appends data to a mock netcdf file"""
    if not os.path.isfile(fname):
        create_empty_netCDF(fname)

    dataset = xr.Dataset(
        {name: data_vars(coordinades)},
        coords=map_coord(coordinades)
    )
    dataset.to_netcdf(path=fname, mode='a')


def create_empty_netCDF(fname):
    """Creates a new empty netCDF file"""
    root_grp = netCDF4.Dataset(fname, 'w', format='NETCDF4')
    root_grp.description = 'Example simulation data'
    root_grp.close()
