"""Fixtures module for pytest"""
import os

from pytest import fixture

from tests.mockup import cf_18 as datamock


@fixture(scope="session", autouse=True)
def dataset_folder(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("data")
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(tmpdir))
    yield
    os.chdir(prevdir)


@fixture(scope="module", params=[datamock.toz_dataset])
def dataset(request):
    return request.param()


@fixture(scope="module", params=["toz_cf18.nc"])
def dataset_file(request, dataset):
    dataset.to_netcdf(request.param)
    return request.param
