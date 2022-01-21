"""Simple test module for testing"""
import subprocess

import iris
from pytest import fail, fixture, mark


@fixture(scope="module")
def paths(netCDF_files):
    return " ".join(netCDF_files)


@fixture(scope="module", params=["1.7"])
def convention(request):
    return request.param


@fixture(scope="class", params=["toz-skimmed"])
def output(request, dataset_folder, operation):
    return f"{dataset_folder}/{request.param}_{operation}.nc"


@fixture(scope="function", params=[""])
def cfcheck(skimmed, convention, output):
    command = f"cfchecks -v {convention} {output}"
    return subprocess.run(command, capture_output=True, shell=True)


@mark.parametrize("operation", ["lon_mean", "lat_mean", "year_mean"], indirect=True)
class TestOperations:
    @fixture(scope="class")
    def operation(self, request):
        return request.param

    @fixture(scope="class", autouse=True)
    def skim_process(self, paths, output, operation):
        command = f"python -m o3skim -o {output} --{operation} {paths}"
        process = subprocess.run(command, capture_output=True, shell=True)
        if process.returncode != 0:
            fail(f"processing failed {process.stderr}")

    @fixture(scope="class")
    def skimmed(self, skim_process, output):
        return iris.load(output)

    def test_originals_not_edited(self, dataset):
        assert dataset

    def test_cf_conventions(self, cfcheck):
        assert cfcheck.returncode == 0
