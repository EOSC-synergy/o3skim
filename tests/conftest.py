"""Fixtures module for pytest"""
import os

from pytest import fixture
import xarray

from tests.mockup import cf_18 as datamock


@fixture(scope="session", autouse=True)
def dataset_folder(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("data")
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(tmpdir))
    yield
    os.chdir(prevdir)


@fixture(scope="module", params=["toz_cf18.nc"])
def netCDF_file(request):
    datamock.toz_dataset(filename=request.param)
    return request.param


@fixture(scope="module")
def dataset(netCDF_file):
    return xarray.open_dataset(netCDF_file)
