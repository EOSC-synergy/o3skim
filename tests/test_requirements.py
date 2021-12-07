"""Simple test module for testing"""
from tests.mockup import cf_19 as datamock
from pytest import fixture


@fixture()
def dataset():
    return datamock.toz_dataset()


def test_simple(dataset):
    dataset.to_netcdf("delete.nc")
    assert True
