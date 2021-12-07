"""Test definitions and groups"""
from pytest import fixture
import o3skim


class Skimmed:
    @fixture(scope="class", autouse=True)  # Required
    def operation(self, request):
        return request.param

    @fixture(scope="class", params=[])  # Default None
    def extra(self, request):
        return request.param

    @fixture(scope="class")
    def operations(self, extra, operation):
        return [operation] + extra

    @fixture(scope="class")
    def skimmed(self, dataset, operations):
        return o3skim.process(dataset, operations)
