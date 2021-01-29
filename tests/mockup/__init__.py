"""Mockup sub-package for tests"""

import numpy as np
import xarray as xr
from tests.mockup import coordinate


def tco3(year_range):
    for year in year_range:
        xr.Dataset(
            data_vars=dict(
                tco3=(["longitude", "latitude", "time"],
                      np.random.rand(21, 11, 12),
                      dict(description="Test tco3 xarray"))
            ),
            coords=dict(
                longitude=coordinate.lon(num=21),
                latitude=coordinate.lat(num=11),
                pressure_level=coordinate.plev(num=4),
                time=coordinate.time(num=12, start=year)
            ),
            attrs=dict(description="Test ozone dataset")
        ).to_netcdf("tco3_{}.nc".format(year))


def vmro3(year_range):
    for year in year_range:
        xr.Dataset(
            data_vars=dict(
                vmro3=(["longitude", "latitude", "pressure_level", "time"],
                       np.random.rand(21, 11, 4, 12),
                       dict(description="Test vmro3 xarray"))
            ),
            coords=dict(
                longitude=coordinate.lon(num=21),
                latitude=coordinate.lat(num=11),
                pressure_level=coordinate.plev(num=4),
                time=coordinate.time(num=12, start=year)
            ),
            attrs=dict(description="Test ozone dataset")
        ).to_netcdf("vmro3_{}.nc".format(year))


def combined(year_range):
    for year in year_range:
        xr.Dataset(
            data_vars=dict(
                tco3=(["longitude", "latitude", "time"],
                      np.random.rand(21, 11, 12),
                      dict(description="Test tco3 xarray")),
                vmro3=(["longitude", "latitude", "pressure_level", "time"],
                       np.random.rand(21, 11, 4, 12),
                       dict(description="Test vmro3 xarray"))
            ),
            coords=dict(
                longitude=coordinate.lon(num=21),
                latitude=coordinate.lat(num=11),
                pressure_level=coordinate.plev(num=4),
                time=coordinate.time(num=12, start=year)
            ),
            attrs=dict(description="Test ozone dataset")
        ).to_netcdf("merged_{}.nc".format(year))


def noise(name='noise'):
    """Some noise that blocks '*' wild card"""
    xr.Dataset(
        data_vars=dict(noise=(["time"], np.random.rand(12))),
        coords=dict(time=coordinate.time(num=12)),
        attrs=dict(description="Test noise dataset")
    ).to_netcdf(name + ".nc")
