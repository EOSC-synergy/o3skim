"""Unittest module template."""

import os
import pytest

import o3skim
import xarray
import tests.mockup as mockup_data

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
                mockup_data.noise(name='merged_noise.nc')
            if source == 'SourceSplit':
                mockup_data.tco3(year_line)
                mockup_data.noise(name='tco3_noise.nc')
                mockup_data.vmro3(year_line)
                mockup_data.noise(name='vmro3_noise.nc')
    with o3skim.utils.cd(data_dir):
        yield data_dir


# Source Tests ------------------------------------------------------
@pytest.fixture(scope='module')
def source_name(request):
    source_name = request.param
    yield source_name


@pytest.fixture(scope='class')
def source(source_name, data_dir):
    yield o3skim.Source(source_name, config[source_name])


@pytest.mark.parametrize('source_name', sources, indirect=True)
class TestSource:

    def test_constructor(self, source_name, data_dir):
        source = o3skim.Source(source_name, config[source_name])
        assert type(source.name) is str
        assert type(source.models) is list

    def test_skimming(self, source):
        assert None == source.skim(groupby=None)
        assert None == source.skim(groupby='year')
        assert None == source.skim(groupby='decade')


# Model Tests ------------------------------------------------------
@pytest.fixture(scope='class')
def model_name(request):
    model_name = request.param
    yield model_name


@pytest.fixture(scope='class')
def model(source, model_name):
    yield source[model_name]


@pytest.mark.parametrize('source_name', sources, indirect=True)
class TestModel:

    @pytest.mark.parametrize('model_name', models, indirect=True)
    def test_model_properties(self, model):
        assert isinstance(model, xarray.Dataset)
        assert model.time.size != 0

    @pytest.mark.parametrize('model_name', ['ModelTCO3'], indirect=True)
    def test_tco3_coordinates(self, model):
        assert 'time' in model.coords
        assert not 'plev' in model.coords
        assert 'lat' in model.coords
        assert 'lon' in model.coords

    @pytest.mark.parametrize('model_name', ['ModelVMRO3'], indirect=True)
    def test_vmro3_coordinates(self, model):
        assert 'time' in model.coords
        assert 'plev' in model.coords
        assert 'lat' in model.coords
        assert 'lon' in model.coords

    @pytest.mark.parametrize('model_name', ['ModelALL'], indirect=True)
    def test_all_coordinates(self, model):
        assert 'time' in model.coords
        assert 'plev' in model.coords
        assert 'lat' in model.coords
        assert 'lon' in model.coords


# Skimming Tests ----------------------------------------------------

@pytest.fixture(scope='class')
def groupby(request):
    return request.param


@pytest.fixture(scope='class')
def skimmed(groupby, source):
    output_dir = "{}_groupby_{}".format(source.name, groupby)
    os.mkdir(output_dir)
    with o3skim.utils.cd(output_dir):
        source.skim(groupby=groupby)
        yield source.name


@pytest.fixture(scope='class')
def skimmed_model(model_name, skimmed):
    source_name = skimmed
    with o3skim.utils.cd(source_name + "_" + model_name):
        yield source_name, model_name


@pytest.mark.parametrize('source_name', sources, indirect=True)
@pytest.mark.parametrize('groupby', [None], indirect=True)
class TestSkimming_NoGroup:

    @pytest.mark.parametrize('model_name', models_tco3, indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        assert os.path.isfile("tco3_zm.nc")

    @pytest.mark.parametrize('model_name', models_vmro, indirect=True)
    def test_skimmed_vmro3(self, skimmed_model):
        assert os.path.isfile("vmro3_zm.nc")


@pytest.mark.parametrize('source_name', sources, indirect=True)
@pytest.mark.parametrize('groupby', ['year'], indirect=True)
class TestSkimming_ByYear:

    @pytest.mark.parametrize('model_name', models_tco3, indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        for y in year_line:
            assert os.path.isfile("tco3_zm_{}-{}.nc".format(y, y + 1))

    @pytest.mark.parametrize('model_name', models_vmro, indirect=True)
    def test_skimmed_vmro3(self, skimmed_model):
        for y in year_line:
            assert os.path.isfile("vmro3_zm_{}-{}.nc".format(y, y + 1))


@pytest.mark.parametrize('source_name', sources, indirect=True)
@pytest.mark.parametrize('groupby', ['decade'], indirect=True)
class TestSkimming_ByDecade:

    @pytest.mark.parametrize('model_name', models_tco3, indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        for y in year_line:
            if y % 10 == 0:
                assert os.path.isfile("tco3_zm_{}-{}.nc".format(y, y + 10))
            else:
                assert not os.path.isfile("tco3_zm_{}-{}.nc".format(y, y + 10))

    @pytest.mark.parametrize('model_name', models_vmro, indirect=True)
    def test_skimmed_vmro3(self, skimmed_model):
        for y in year_line:
            if y % 10 == 0:
                assert os.path.isfile("vmro3_zm_{}-{}.nc".format(y, y + 10))
            else:
                assert not os.path.isfile("vmro3_zm_{}-{}.nc".format(y, y + 10))
