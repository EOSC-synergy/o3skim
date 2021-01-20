"""Unittest module template."""

import os
import pytest

import o3skim
import xarray
import tests.mockup_data as mockup_data


# Test configurations ----------------------------------------------
configuration_file = "tests/sources_err.yaml"
year_line = range(2000, 2022)

sources = ["SourceSplit"]
# models = ["ModelBadName", "ModelBadPath", "ModelMissingCoords",
#           "ModelBadCoords", "ModelExtraCoords"]

config = o3skim.utils.load(configuration_file)


# Module fixtures ---------------------------------------------------
@ pytest.fixture(scope='module')
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
@ pytest.fixture(scope='module')
def source_config(request, data_dir):
    source_name = request.param
    yield source_name, config[source_name]


@ pytest.fixture(scope='class')
def source(source_config):
    source_name, collections = source_config
    yield o3skim.Source(source_name, collections)


@ pytest.mark.parametrize('source_config', sources, indirect=True)
class Test_Exceptions:

    def test_constructor(self, source_config):
        source_name, collections = source_config
        source = o3skim.Source(source_name, collections)
        assert source.name == source_name
        assert source.models == []
        assert True

    def test_skimming(self, source):
        assert None == source.skim(groupby=None)
        assert None == source.skim(groupby='year')
        assert None == source.skim(groupby='decade')
        assert True

