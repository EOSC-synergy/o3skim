"""Fixtures module for pytest"""
import os

import o3mocks
import xarray
from pytest import fixture


@fixture(scope="session", autouse=True)
def dataset_folder(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("data")
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(tmpdir))
    yield
    os.chdir(prevdir)


@fixture(scope="module", params=["toz_cf18.nc"])
def netCDF_file(request):
    o3mocks.cf_18.toz_dataset(filename=request.param)
    return request.param


@fixture(scope="module")
def dataset(netCDF_file):
    return xarray.open_dataset(netCDF_file)
