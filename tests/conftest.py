"""Fixtures module for pytest"""
import xarray as xr
from pytest import fixture


@fixture(
    scope="session",
    params=[
        "tests/datasets/toz_std.1.8.nc",
        "tests/datasets/no_bounds/*.nc",
        "tests/datasets/no_cellmx/*.nc",
        "tests/datasets/splitted/*.nc",
    ],
)
def dataset_path(request):
    return request.param


@fixture(scope="session")
def dataset(dataset_path, variable):
    kwargs = dict(data_vars='minimal', concat_dim='time', combine='nested')
    with xr.open_mfdataset(dataset_path, **kwargs) as ds:
        yield ds.cf[[variable]]


@fixture(scope="session")
def variable():
    return "atmosphere_mole_content_of_ozone"
