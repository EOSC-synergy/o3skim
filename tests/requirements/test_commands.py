"""Simple test module for testing"""
import subprocess

import cf_xarray as cfxr
import xarray as xr
from pytest import fixture, mark, skip


@fixture(scope="module")
def paths(netCDF_files):
    return " ".join(netCDF_files)


@fixture(scope="module", params=["toz-skimmed.nc"])
def output(request):
    return request.param


@fixture(scope="module", params=["lon_mean", "lat_mean", "year_mean"])
def operation(request):
    return request.param


@fixture(scope="module", autouse=True)
def process(paths, output, operation):
    command = f"python -m o3skim -o {output} --{operation} {paths}"
    return subprocess.run(command, shell=True)


@fixture(scope="module")
def skimmed(process, output):
    if process.returncode != 0:
        skip("processing failed, no sense to continue")
    return xr.open_dataset(output)


@fixture(scope="module")
def conventions(skimmed, output):
    command = f"cfchecks {output}"
    return subprocess.run(command, shell=True)


def test_command_success(process):
    assert process.returncode == 0


@mark.usefixtures("skimmed")
def test_originals_not_edited(dataset):
    assert dataset


@mark.usefixtures("skimmed")
def test_cf_conventions(conventions):
    assert conventions.returncode == 0
