"""Fixtures module for pytest"""
from pytest import fixture
import o3skim


@fixture(scope="class", params=[])
def operations(request):
    return request.param


@fixture(scope="class")
def skimmed(dataset, operations):
    return o3skim.process(dataset, operations)
