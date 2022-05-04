"""Fixtures module for pytest"""
import xarray as xr
from pytest import fixture
from os import listdir


@fixture(scope="session", params=listdir("tests/datasets/CCMI-1"))
def CCMI_model(request):
    return request.param


@fixture(scope="session", params=listdir("tests/datasets/ESACCI"))
def ESACCI_model(request):
    return request.param


@fixture(scope="session", params=listdir("tests/datasets/SBUV"))
def SBUV_model(request):
    return request.param
