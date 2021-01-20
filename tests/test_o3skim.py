"""Unittest module template."""

import os
import pytest

import o3skim
import xarray
import tests.mockup_data as mockup_data

# Test configurations ----------------------------------------------
configuration_file = "tests/sources_example.yaml"
year_line = range(2000, 2022)

sources = ["SourceSplit", "SourceMerged"]
models = ["ModelTCO3", "ModelVMRO3", "ModelALL"]

models_tco3 = ['ModelTCO3', 'ModelALL']
models_vmro = ['ModelVMRO3', 'ModelALL']

config = o3skim.utils.load(configuration_file)


# Module fixtures ---------------------------------------------------
@pytest.fixture(scope='module')
def data_dir(tmpdir_factory):
    data_dir = tmpdir_factory.mktemp("data")
    for source in sources:
        source_dir = data_dir.join(source)
        os.mkdir(source_dir)
        with o3skim.utils.cd(source_dir):
            if source == 'SourceMerged':
                mockup_data.combined(year_line)

            if source == 'SourceSplit':
                mockup_data.tco3(year_line)
                mockup_data.vmro3(year_line)

    with o3skim.utils.cd(data_dir):
        yield data_dir


# Source Tests ------------------------------------------------------
@pytest.fixture(scope='module')
def source_config(request, data_dir):
    source_name = request.param
    yield source_name, config[source_name]


@pytest.fixture(scope='class')
def source(source_config):
    source_name, collections = source_config
    yield o3skim.Source(source_name, collections)


@pytest.mark.parametrize('source_config', sources, indirect=True)
class TestSource:

    def test_constructor(self, source_config):
        source_name, collections = source_config
        source = o3skim.Source(source_name, collections)
        assert type(source.name) is str
        assert type(source.models) is list
        for model in source.models:
            assert isinstance(source[model], o3skim.Model)
            assert source[model].time.size != 0

    def test_skimming(self, source):
        assert None == source.skim(groupby=None)
        assert None == source.skim(groupby='year')
        assert None == source.skim(groupby='decade')


# Model Tests ------------------------------------------------------
@pytest.fixture(scope='class')
def model_config(request, source_config):
    _, source_config = source_config
    model_name = request.param
    yield model_name, source_config[model_name]


@pytest.fixture(scope='class')
def model(model_config):
    _, specifications = model_config
    yield o3skim.Model(specifications)


@pytest.mark.parametrize('source_config', sources, indirect=True)
class TestModel:

    @pytest.mark.parametrize('model_config', models, indirect=True)
    def test_constructor(self, model_config):
        _model_name, specifications = model_config
        model = o3skim.Model(specifications)
        assert isinstance(model, xarray.Dataset)
        assert model.time.size != 0

    @pytest.mark.parametrize('model_config', models_tco3, indirect=True)
    def test_tco3_coordinates(self, model):
        assert 'time' in model["tco3_zm"].coords
        assert 'lat' in model["tco3_zm"].coords
        assert not 'plev' in model["tco3_zm"].coords
        assert not 'lon' in model["tco3_zm"].coords

    @pytest.mark.parametrize('model_config', models_vmro, indirect=True)
    def test_vmro3_coordinates(self, model):
        assert 'time' in model["vmro3_zm"].coords
        assert 'lat' in model["vmro3_zm"].coords
        assert 'plev' in model["vmro3_zm"].coords
        assert not 'lon' in model["vmro3_zm"].coords


# Skimming Tests ----------------------------------------------------
@pytest.fixture(scope='class')
def skimmed(request, source):
    groupby = request.param
    output_dir = source.name + "_group_" + str(groupby)
    os.mkdir(output_dir)
    with o3skim.utils.cd(output_dir):
        source.skim(groupby=groupby)
        yield source.name


@pytest.fixture(scope='class')
def skimmed_model(model_config, skimmed):
    source_name = skimmed
    model_name, _ = model_config
    with o3skim.utils.cd(source_name + "_" + model_name):
        yield source_name, model_name


@pytest.mark.parametrize('source_config', sources, indirect=True)
@pytest.mark.parametrize('skimmed', [None], indirect=True)
class TestSkimming_NoGroup:

    @pytest.mark.parametrize('model_config', models_tco3, indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        assert os.path.isfile("tco3_zm.nc")

    @pytest.mark.parametrize('model_config', models_vmro, indirect=True)
    def test_skimmed_vmro3(self, skimmed_model):
        assert os.path.isfile("vmro3_zm.nc")


@pytest.mark.parametrize('source_config', sources, indirect=True)
@pytest.mark.parametrize('skimmed', ['year'], indirect=True)
class TestSkimming_ByYear:

    @pytest.mark.parametrize('model_config', models_tco3, indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        for y in year_line:
            assert os.path.isfile("tco3_zm_{}-{}.nc".format(y, y + 1))

    @pytest.mark.parametrize('model_config', models_vmro, indirect=True)
    def test_skimmed_vmro3(self, skimmed_model):
        for y in year_line:
            assert os.path.isfile("vmro3_zm_{}-{}.nc".format(y, y + 1))


@pytest.mark.parametrize('source_config', sources, indirect=True)
@pytest.mark.parametrize('skimmed', ['decade'], indirect=True)
class TestSkimming_ByDecade:

    @pytest.mark.parametrize('model_config', models_tco3, indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        for y in year_line:
            if y % 10 == 0:
                assert os.path.isfile("tco3_zm_{}-{}.nc".format(y, y + 10))

    @pytest.mark.parametrize('model_config', models_vmro, indirect=True)
    def test_skimmed_vmro3(self, skimmed_model):
        for y in year_line:
            if y % 10 == 0:
                assert os.path.isfile("vmro3_zm_{}-{}.nc".format(y, y + 10))
