"""Mockup sub-package for tests"""
import pandas as pd
import numpy as np
import xarray as xr
from tests.mockup import coordinate, datarray


def data(year_range, data_format, timeline):
    if data_format == 'merged':
        [combined(y, timeline) for y in year_range]
    elif data_format == 'splitted':
        [tco3(y, timeline) for y in year_range]
        [vmro3(y, timeline) for y in year_range]


def tco3(year, timeline):
    """Creates netCDF files with tco3 data variable"""
    dataset = xr.Dataset(
        data_vars=dict(tco3=datarray.random_tco3(year)),
        attrs=dict(description="Test ozone dataset"))
    if timeline == 'time_coord':
        dataset.to_netcdf("tco3_{}.nc".format(year))
    elif timeline == 'time_name':
        save_with_timestamp(dataset, prefix='tco3')


def vmro3(year, timeline):
    """Creates netCDF files with vmro3 data variable"""
    dataset = xr.Dataset(
        data_vars=dict(vmro3=datarray.random_vmro3(year)),
        attrs=dict(description="Test ozone dataset"))
    if timeline == 'time_coord':
        dataset.to_netcdf("vmro3_{}.nc".format(year))
    elif timeline == 'time_name':
        save_with_timestamp(dataset, prefix='vmro3')


def combined(year, timeline):
    """Creates combined netCDF files with o3 data variables"""
    dataset = xr.Dataset(
        data_vars=dict(
            tco3=datarray.random_tco3(year),
            vmro3=datarray.random_vmro3(year)),
        attrs=dict(description="Test ozone dataset"))
    if timeline == 'time_coord':
        dataset.to_netcdf("merged_{}.nc".format(year))
    elif timeline == 'time_name':
        save_with_timestamp(dataset, prefix='merged')


def save_with_timestamp(dataset, prefix):
    tx, dsx = zip(*dataset.groupby("time"))
    def date(t): return pd.to_datetime(t).date()
    xr.save_mfdataset(
        [ds.drop('time') for ds in dsx],
        ['{}_{}.nc'.format(prefix, date(t)) for t in tx])


def noise(name='noise'):
    """Some noise that blocks '*' wild card"""
    xr.Dataset(
        data_vars=dict(noise=(["time"], np.random.rand(12))),
        coords=dict(time=coordinate.time(num=12)),
        attrs=dict(description="Test noise dataset")
    ).to_netcdf(name + ".nc")
