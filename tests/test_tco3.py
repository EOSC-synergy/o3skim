"""Pytest module to test tco3 data as blackbox."""

import os

import o3skim
import pytest
import tests.conftest as conftest
import xarray


def pytest_generate_tests(metafunc):
    config_file = conftest.sources_example
    metafunc.parametrize("config_file", [config_file], indirect=True)
    metafunc.parametrize("source_name", conftest.sources, indirect=True)
    metafunc.parametrize("variable", ["tco3_zm"], indirect=True)


class TestModel:

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    def test_tco3_coordinates(self, model, variable):
        assert 'time' in model.coords
        assert 'lat' in model.coords
        assert 'lon' in model.coords

    @pytest.mark.parametrize('model_name', ["ModelTCO3"], indirect=True)
    def test_tco3_no_extra_coordinates(self, model, variable):
        assert len(model.coords) == 3


@pytest.mark.parametrize('groupby', [None], indirect=True)
class TestSkimming_NoGroup:

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', [None], indirect=True)
    def test_isTCO3file(self, skimed_file):
        assert os.path.isfile(skimed_file)

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', [None], indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        assert 'tco3_zm' in skimmed_model.var()
        assert 'time' in skimmed_model.coords
        assert not 'plev' in skimmed_model.coords
        assert 'lat' in skimmed_model.coords
        assert not 'lon' in skimmed_model.coords


@pytest.mark.parametrize('groupby', ['year'], indirect=True)
class TestSkimming_ByYear:

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', list(conftest.year_line), indirect=True)
    def test_isTCO3file(self, skimed_file):
        assert os.path.isfile(skimed_file)

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', list(conftest.year_line), indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        assert 'tco3_zm' in skimmed_model.var()
        assert 'time' in skimmed_model.coords
        assert not 'plev' in skimmed_model.coords
        assert 'lat' in skimmed_model.coords
        assert not 'lon' in skimmed_model.coords


@pytest.mark.parametrize('groupby', ['decade'], indirect=True)
class TestSkimming_ByDecade:

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', [y for y in conftest.year_line if y % 10 == 0], indirect=True)
    def test_isTCO3file(self, skimed_file):
        assert os.path.isfile(skimed_file)

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', [y for y in conftest.year_line if y % 10 != 0], indirect=True)
    def test_isNotTCO3file(self, skimed_file, year):
        assert not os.path.isfile(skimed_file)

    @pytest.mark.parametrize('model_name', conftest.models_tco3, indirect=True)
    @pytest.mark.parametrize('year', [y for y in conftest.year_line if y % 10 == 0], indirect=True)
    def test_skimmed_tco3(self, skimmed_model):
        assert 'tco3_zm' in skimmed_model.var()
        assert 'time' in skimmed_model.coords
        assert not 'plev' in skimmed_model.coords
        assert 'lat' in skimmed_model.coords
        assert not 'lon' in skimmed_model.coords
