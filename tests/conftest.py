"""Pytest configuration file."""

import os

import o3skim
import pytest
import tests.mockup as mockup_data
import xarray

# configurations ----------------------------------------------------
year_line = range(2000, 2022)

sources = ["SourceSplit", "SourceMerged"]
sources_example = "tests/sources_example.yaml"
sources_err = "tests/sources_err.yaml"

models = ["ModelTCO3", "ModelVMRO3", "ModelALL"]
models_tco3 = ['ModelTCO3', 'ModelALL']
models_vmro3 = ['ModelVMRO3', 'ModelALL']


# session fixtures ---------------------------------------------------
@pytest.fixture(scope='session')
def data_dir(tmpdir_factory):
    data_dir = tmpdir_factory.mktemp("data")
    for source in sources:
        source_dir = data_dir.join(source)
        os.mkdir(source_dir)
        with o3skim.utils.cd(source_dir):
            if source == 'SourceMerged':
                mockup_data.combined(year_line)
                mockup_data.noise(name='merged_noise.nc')
            if source == 'SourceSplit':
                mockup_data.tco3(year_line)
                mockup_data.noise(name='tco3_noise.nc')
                mockup_data.vmro3(year_line)
                mockup_data.noise(name='vmro3_noise.nc')
    return data_dir


@pytest.fixture(scope='session')
def config_file(request):
    return request.param


@pytest.fixture(scope='session')
def config_dict(config_file):
    return o3skim.utils.load(config_file)


# package fixtures --------------------------------------------------


# module fixtures ---------------------------------------------------
@pytest.fixture(scope='module')
def output_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("output")


@pytest.fixture(scope='module')
def groupby(request):
    return request.param


@pytest.fixture(scope='module')
def source_name(request):
    return request.param


@pytest.fixture(scope='module')
def source(config_dict, source_name, data_dir):
    with o3skim.utils.cd(data_dir):
        source = o3skim.Source(source_name, config_dict[source_name])
    return source


@pytest.fixture(scope='module')
def skimmed(groupby, source, output_dir):
    with o3skim.utils.cd(output_dir):
        source.skim(groupby=groupby)
        yield groupby, source.name


# class fixtures --------------------------------------------------


# function fixtures -------------------------------------------------
@pytest.fixture()
def model_name(request):
    return request.param


@pytest.fixture()
def model(source, model_name):
    return source[model_name]


@pytest.fixture()
def year(request):
    return request.param


@pytest.fixture()
def variable(request):
    return request.param


@pytest.fixture()
def skimed_file(skimmed, model_name, variable, year):
    groupby, source_name = skimmed
    with o3skim.utils.cd("{}_{}".format(source_name, model_name)):
        if not groupby:
            yield "{}.nc".format(variable)
        if groupby == 'year':
            yield "{}_{}-{}.nc".format(variable, year, year + 1)
        if groupby == 'decade':
            yield "{}_{}-{}.nc".format(variable, year, year + 10)


@pytest.fixture()
def skimmed_model(skimed_file):
    with xarray.open_dataset(skimed_file) as model:
        yield model
