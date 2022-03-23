"""Fixtures module for pytest"""
from pytest import fixture
import o3skim


@fixture(scope="class", params=[])
def operations(request):
    return request.param


@fixture(scope="class")
def skimmed(dataset, operations):
    return o3skim.process(dataset, operations)


@fixture(scope="class")
def standard_name(skimmed):
    return skimmed["toz_zm"].attrs["standard_name"]


@fixture(scope="class")
def units(skimmed):
    return skimmed["toz_zm"].attrs["units"]


@fixture(scope="class")
def cell_methods(skimmed):
    return skimmed["toz_zm"].attrs["cell_methods"]
