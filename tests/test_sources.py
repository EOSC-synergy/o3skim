"""Pytest module to test sources as blackbox."""

import os

import o3skim
import pytest
import tests.conftest as conftest
import xarray


@pytest.mark.parametrize('config_file', [conftest.sources_example], indirect=True)
@pytest.mark.parametrize('source_name', conftest.sources, indirect=True)
class TestSource:

    def test_constructor(self, config_dict, source_name, data_dir):
        with o3skim.utils.cd(data_dir):
            source = o3skim.Source(source_name, config_dict[source_name])
            assert type(source.name) is str
            assert type(source.models) is list
            assert source.models != []

    def test_skimming(self, source, output_dir):
        with o3skim.utils.cd(output_dir):
            assert None == source.skim(groupby=None)
            assert None == source.skim(groupby='year')
            assert None == source.skim(groupby='decade')

    @pytest.mark.parametrize('model_name', conftest.models, indirect=True)
    def test_model_properties(self, model):
        assert isinstance(model, xarray.Dataset)
        assert model.time.size != 0


@pytest.mark.parametrize('config_file', [conftest.sources_err], indirect=True)
@pytest.mark.parametrize('source_name', ["SourceSplit"], indirect=True)
class TestExceptions:

    def test_constructor(self, config_dict, source_name, data_dir):
        with o3skim.utils.cd(data_dir):
            source = o3skim.Source(source_name, config_dict[source_name])
            assert source.name == source_name
            assert source.models == []
            assert True

    def test_skimming(self, source):
        assert None == source.skim(groupby=None)
        assert None == source.skim(groupby='year')
        assert None == source.skim(groupby='decade')
        assert True
