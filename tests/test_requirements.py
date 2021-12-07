"""Simple test module for testing"""
import os

from pytest import fixture

from tests.mockup import cf_19 as datamock


@fixture(scope="session")
def dataset_folder(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("data")
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(tmpdir))
    yield
    os.chdir(prevdir)


@fixture(scope="module", params=["toz_cf19.nc"])
def dataset_file(request, dataset_folder):
    datamock.toz_dataset().to_netcdf(request.param)
    return request.param


def test_simple(dataset_file):
    assert True
