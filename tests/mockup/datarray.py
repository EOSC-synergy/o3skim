"""Module with DataArray mockups"""
import numpy as np
import xarray as xr
from tests.mockup import coordinate


def random_tco3(year):
    """Test tco3 xarray"""
    coordinates = dict(
        longitude=coordinate.lon(num=21),
        latitude=coordinate.lat(num=11),
        time=coordinate.time(num=12, start=year))
    return random(coordinates, random_tco3.__doc__)


def random_vmro3(year):
    """Test vmro3 xarray"""
    coordinates = dict(
        longitude=coordinate.lon(num=21),
        latitude=coordinate.lat(num=11),
        pressure_level=coordinate.plev(num=4),
        time=coordinate.time(num=12, start=year))
    return random(coordinates, random_vmro3.__doc__)


def random(coordinates, description=""):
    dimensions = [len(v) for _, v in coordinates.items()]
    return xr.DataArray(
        data=np.random.rand(*dimensions),
        attrs={'description': description},
        coords=coordinates,
        dims=list(coordinates))
