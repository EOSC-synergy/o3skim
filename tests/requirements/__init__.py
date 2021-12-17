"""Test definitions and groups"""
import xarray as xr
from o3skim import __main__
from pytest import fixture

import o3skim


class Skimmed:
    @fixture(scope="class", autouse=True)  # Needs parametrization
    def operation(self, request):
        return request.param

    @fixture(scope="class")
    def operations(self, operation):
        return [operation]

    @fixture(scope="class")
    def skimmed(self, dataset, operations):
        return o3skim.process(dataset, operations)
