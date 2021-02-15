"""Pytest configuration file."""

import os

import o3skim
import pytest
import tests.mockup as mockup_data
import xarray

# configurations ----------------------------------------------------
year_line = range(2000, 2022)

#  Source files
sources_example = "tests/sources_example.yaml"
sources_err = "tests/sources_err.yaml"
available_configurations = {
    'correct': {sources_example},
    'errors': {sources_err}
}

# Sources
sources = ["SourceSplit", "SourceMerged"]

# Models
tco3_models = {
    'SourceSplit_ModelTCO3',
    'SourceSplit_ModelALL',
    'SourceMerged_ModelTCO3',
    'SourceMerged_ModelALL'
}
vmro3_models = {
    'SourceSplit_ModelVMRO3',
    'SourceSplit_ModelALL',
    'SourceMerged_ModelVMRO3',
    'SourceMerged_ModelALL'
}
error_models = {
    'ModelBadVar',
    'ModelBadKey',
    'ModelBadName',
    'ModelBadPath',
    'ModelMissingCoords',
    'ModelBadCoords',
    'ModelExtraCoords'
}
available_models = {
    'all': tco3_models | vmro3_models,
    'with_tco3': tco3_models,
    'only_tco3': tco3_models - vmro3_models,
    'with_vmro3': vmro3_models,
    'only_vmro3': vmro3_models - tco3_models,
    'errors': error_models
}


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
def output_dir(tmpdir_factory, groupby, model):
    output_dir = tmpdir_factory.mktemp(model + "_by_" + str(groupby))
    return output_dir


@pytest.fixture(scope='session')
def metadata_dir(tmpdir_factory, model):
    metadata_dir = tmpdir_factory.mktemp(model + "_metadata")
    return metadata_dir


@pytest.fixture(scope='session')
def config(request):
    return request.param


@pytest.fixture(scope='session')
def model(request):
    return request.param


@pytest.fixture(scope='session')
def config_dict(config):
    return o3skim.utils.load(config)


@pytest.fixture(scope='session')
def model_config(config_dict, model):
    return config_dict[model]


@pytest.fixture(scope='session')
def load_model(data_dir, model_config):
    with o3skim.utils.cd(data_dir):
        return o3skim.loading(**model_config)


@pytest.fixture(scope='session')
def dataset(load_model):
    dataset, metadata = load_model
    return dataset


@pytest.fixture(scope='session')
def metadata(load_model):
    dataset, metadata = load_model
    return metadata


@pytest.fixture(scope='session')
def actions(request):
    return request.param


@pytest.fixture(scope='session')
def processed(dataset, actions):
    return o3skim.processing(dataset, actions)


@pytest.fixture(scope='session')
def groupby(request):
    return request.param


@pytest.fixture(scope='session')
def splitted(dataset, groupby):
    return o3skim.grouping(dataset, split_by=groupby)


@pytest.fixture(scope='session')
def years(splitted):
    years, splitted_ds = splitted
    return years


@pytest.fixture(scope='session')
def splitted_ds(splitted):
    years, splitted_ds = splitted
    return splitted_ds


@pytest.fixture(scope='session')
def variables(model):
    variables = []
    if model in available_models['with_tco3']:
        variables.append('tco3_zm')
    if model in available_models['with_vmro3']:
        variables.append('vmro3_zm')
    return variables


@pytest.fixture(scope='session')
def expected_netCDF(groupby, variables):
    if groupby == None:
        return ["{}.nc".format(v)
                for v in variables]
    elif groupby == 'year':
        def format(v, y): return "{}_{}-{}.nc".format(v, y, y+1)
        return [format(v, y)
                for y in year_line
                for v in variables]
    elif groupby == 'decade':
        def format(v, y): return "{}_{}-{}.nc".format(v, y, y+10)
        return [format(v, y)
                for y in year_line if y % 10 == 0
                for v in variables]
    else:
        raise KeyError("bad groupby {}".format(groupby))


@pytest.fixture(scope='session')
def save_netCDF(output_dir, splitted_ds, groupby, years):
    with o3skim.utils.cd(output_dir):
        o3skim.saving(splitted_ds, groupby, years)


@pytest.fixture(scope='session')
def saved_ds(output_dir, save_netCDF, expected_netCDF):
    with o3skim.utils.cd(output_dir):
        return xarray.open_mfdataset(expected_netCDF)


@pytest.fixture(scope='session')
def save_metadata(metadata_dir, metadata):
    with o3skim.utils.cd(metadata_dir):
        o3skim.utils.save("metadata.yaml", metadata)


@pytest.fixture(scope='session')
def metadata_file_content(metadata_dir, save_metadata):
    with o3skim.utils.cd(metadata_dir):
        return o3skim.utils.load("metadata.yaml")


# package fixtures --------------------------------------------------


# module fixtures ---------------------------------------------------


# class fixtures --------------------------------------------------


# function fixtures -------------------------------------------------
@pytest.fixture()
def data_cd(data_dir):
    with o3skim.utils.cd(data_dir):
        yield None


@pytest.fixture()
def output_cd(output_dir):
    with o3skim.utils.cd(output_dir):
        yield None


@pytest.fixture()
def metadata_cd(metadata_dir):
    with o3skim.utils.cd(metadata_dir):
        yield None
