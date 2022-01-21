"""Fixtures module for pytest"""
import os

import cf
import iris
import o3mocks
import xarray as xr
from pytest import fixture


@fixture(scope="session", autouse=True)
def dataset_folder(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("data")
    return os.path.expanduser(tmpdir)


@fixture(scope="module", params=["toz_cf18"])
def netCDF_file(request, dataset_folder):
    filename = f"{dataset_folder}/{request.param}.nc"
    o3mocks.cf_18.toz_dataset(filename)
    return filename


@fixture(scope="module")
def netCDF_files(netCDF_file):
    ds = xr.open_dataset(netCDF_file)
    dates, datasets = zip(*ds.groupby("time"))
    paths = [f"{netCDF_file[:-3]}_{t}.nc" for t in dates]
    xr.save_mfdataset(datasets, paths)
    return paths


# @fixture(scope="module")
# def dataset(netCDF_files):
#     return xr.open_mfdataset(
#         paths=netCDF_files,
#         concat_dim="time",
#         combine="nested",
#     )


# @fixture(scope="module")
# def dataset(netCDF_file):
#     return cf.read(netCDF_file)[0]


@fixture(scope="module")
def dataset(netCDF_files):
    return iris.load_cube(netCDF_files, "atmosphere_mole_content_of_ozone")
