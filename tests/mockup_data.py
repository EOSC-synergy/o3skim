"""This modules creates mockup data for testing"""

import xarray as xr
import numpy as np


start = {'time':  0, 'plev':    0, 'lat': -90, 'lon': -180}
end = {'time': 20, 'plev': 1000, 'lat': +90, 'lon': +180}
step = {'time':  1, 'plev':  100, 'lat':  10, 'lon':   10}
size = {'time': 20, 'plev':   10, 'lat':  18, 'lon':   36}


def data_vars(coordinades):
    alias = tuple(coordinades.values())
    dim = tuple(size[c] for c in coordinades)
    return alias, np.ones(dim),


def map_coord(coordinades):
    return {alias: [x for x in range(start[c], end[c], step[c])]
            for c, alias in coordinades.items()}


def netcdf(path, name, coordinades, **kwarg):
    dataset = xr.Dataset(
        {name: data_vars(coordinades)},
        coords=map_coord(coordinades)
    )
    dataset.to_netcdf(path=path, mode='a')
