"""Fixtures module for pytest"""
from pytest import fixture, xfail
import o3skim


@fixture(scope="class", params=[])
def operations(request):
    return request.param


@fixture(scope="class")
def skimmed(dataset, operations):
    return o3skim.process(dataset, operations)


@fixture(scope="class")
def standard_name(skimmed, variable):
    return skimmed.cf[variable].attrs["standard_name"]


@fixture(scope="class")
def units(skimmed, variable):
    return skimmed.cf[variable].attrs["units"]


@fixture(scope="class")
def cell_methods(dataset, skimmed, variable):
    if "cell_methods" in dataset.cf[variable].attrs:
        return skimmed.cf[variable].attrs["cell_methods"]
    else:
        xfail("Cell methods not in original dataset")
