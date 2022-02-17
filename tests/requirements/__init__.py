"""Test definitions and groups"""
import o3skim
from pytest import fixture


class Skimmed:
    @fixture(scope="class", autouse=True)  # Req. parametrization
    def operation(self, request):
        return request.param

    @fixture(scope="class")
    def operations(self, operation):
        return [operation]

    @fixture(scope="class")
    def skimmed(self, dataset, operations):
        return o3skim.process(dataset, operations)
