"""Pytest configuration file."""
from o3skim.scripts import o3norm
import os

import o3skim
import pytest
from tests.mockup import ccmi, ecmwf, esacci
import tests.mockup as mockup_data
import xarray

# configurations ----------------------------------------------------
year_line = range(2000, 2020)
var_names = {
    'ccmi':  dict(tco3_zm='toz', vmro3_zm='vmro3'),
    'ecmwf': dict(tco3_zm='tco3', vmro3_zm='vmro3'),
    'esacci': dict(tco3_zm='tco3', vmro3_zm='vmro3')}


# session fixtures --------------------------------------------------
@pytest.fixture(scope='session')
def source(request):
    return request.param


@pytest.fixture(scope='session')
def variable(request):
    return request.param


@pytest.fixture(scope='session')
def paths(tmpdir_factory, source, variable):
    source_dir = tmpdir_factory.mktemp(source + '_' + variable)
    with o3skim.utils.cd(source_dir):
        if source == 'ccmi':
            ccmi.create_data(variable, year_line)
        if source == 'ecmwf':
            ecmwf.create_data(year_line)  # Merged
        if source == 'esacci':
            esacci.create_data(year_line)  # Merged
        files = os.listdir()
    return [str(source_dir.join(f)) for f in files]


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
    return str(output_dir.join('o3data.nc'))


@pytest.fixture()
def var_name(source, variable):
    return var_names[source][variable]
