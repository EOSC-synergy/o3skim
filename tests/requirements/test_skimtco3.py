"""Simple test module for testing"""
import argparse

import xarray as xr
from pytest import fail, fixture, mark
import o3skim.scripts.skim_tco3 as skim_tco3


@fixture(scope="module")
def paths(dataset_path):
    return dataset_path


@fixture(scope="module")
def operations(lon_mean, lat_mean):
    operations = []
    if lon_mean:
        operations.append("lon_mean")
    if lat_mean:
        operations.append("lat_mean")
    return operations if operations else None


@fixture(scope="module", params=[False, True])
def lon_mean(request):
    return request.param


@fixture(scope="module", params=[False, True])
def lat_mean(request):
    return request.param


@fixture(scope="module", params=["atmosphere_mole_content_of_ozone"])
def variable_name(request):
    return request.param


@fixture(scope="module")
def options(verbosity, output, original_attributes):
    return dict(
        verbosity=verbosity,
        output=output,
        original_attributes=original_attributes,
    )


@fixture(scope="module", params=["DEBUG", "ERROR"])
def verbosity(request):
    return request.param


@fixture(scope="module", params=["toz-skimmed.nc"])
def output(request):
    return request.param


@fixture(scope="module", params=[False])
def original_attributes(request):
    return request.param


def test_something(paths, operations, variable_name, options):
    skim_tco3.process(paths, operations, variable_name, **options)
