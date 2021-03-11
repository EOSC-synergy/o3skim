"""Pytest configuration file."""
import glob
import o3skim
import os
import pytest
from tests.mockup import standard
from tests.mockup import ccmi, ecmwf, esacci, sbuv
from tests.utils import cd
import xarray as xr


# configurations ----------------------------------------------------
year_line = range(2000, 2020)


# session fixtures --------------------------------------------------


# package fixtures --------------------------------------------------


# module fixtures ---------------------------------------------------


# class fixtures ----------------------------------------------------


# function fixtures -------------------------------------------------
@pytest.fixture()
def output_dir(tmpdir_factory):
    output_dir = tmpdir_factory.mktemp("output")
    return output_dir


@pytest.fixture()
def target(output_dir):
    target = output_dir.join('target')
    os.makedirs(target)
    return f"{target}/o3data"


@pytest.fixture()
def output(output_dir):
    output = output_dir.join('output')
    os.makedirs(output)
    return str(output)


@pytest.fixture()
def variable(request):
    return request.param


@pytest.fixture()
def tco3_ds():
    dsx = [standard.random_tco3_dataset(y) for y in range(2000, 2022)]
    return xr.concat(dsx, dim='time')


@pytest.fixture()
def vmro3_ds():
    dsx = [standard.random_vmro3_dataset(y) for y in range(2000, 2022)]
    return xr.concat(dsx, dim='time')


@pytest.fixture()
def random_dataset():
    dsx = [standard.random_dataset(y) for y in range(2000, 2022)]
    return xr.concat(dsx, dim='time')


@pytest.fixture()
def split_by(request):
    return request.param


@pytest.fixture()
def operations(request):
    return request.param


@pytest.fixture()
def source(request):
    return request.param


@pytest.fixture()
def source_files(tmpdir_factory, source, variable):
    source_dir = tmpdir_factory.mktemp(source + '_' + variable)
    with cd(source_dir):
        if source == 'CCMI-1':
            ccmi.create_data(variable, year_line)
        if source == 'ECMWF':
            ecmwf.create_data(year_line)  # Merged
        if source == 'ESACCI':
            esacci.create_data(year_line)  # Merged
        if source == 'SBUV':
            sbuv.create_data(year_line)  # Merged
        files = os.listdir()
    return [str(source_dir.join(f)) for f in files]


@pytest.fixture()
def o3data_files(random_dataset, target, split_by):
    o3skim.save(random_dataset, target, split_by)
    return glob.glob(f"{target}*")
