"""Mockup sub-package for tests"""
import pandas as pd
import numpy as np
import xarray as xr


def dataset_from(**arrays):
    return xr.Dataset(
        data_vars=arrays,
        attrs=dict(description="Test ozone dataset"))


def random_array(coordinates, description):
    dimensions = [len(v) for _, v in coordinates.items()]
    return xr.DataArray(
        data=np.random.rand(*dimensions),
        attrs={'description': description},
        coords=coordinates,
        dims=list(coordinates))


def random_noise(name='noise'):
    xr.Dataset(
        data_vars=dict(noise=(["time"], np.random.rand(12))),
        coords=dict(time=time(num=12)),
        attrs=dict(description="Test noise dataset")
    ).to_netcdf(name + ".nc")


def time(num=12, start=2000, end=None):
    end = start + 1 if not end else end
    start = pd.Timestamp("{}-01-01".format(start))
    end = pd.Timestamp("{}-01-01".format(end))
    t = np.linspace(start.value, end.value, num + 1)[0:-1]
    return pd.to_datetime(t)


def lat(num=11):
    return np.linspace(-90, 90, num)


def lon(num=21):
    return np.linspace(-180, 180, num)


def plev(num=4):
    return np.logspace(1, 4, num)
