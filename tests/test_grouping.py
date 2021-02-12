"""Pytest module to test sources as blackbox."""
import o3skim
import pytest
import tests.conftest as conftest

configs = conftest.available_configurations
models = conftest.available_models


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('groupby', [None], indirect=True)
class TestNone:

    def test_years(self, years):
        assert years == [None]

    def test_splitted_datasets(self, dataset, splitted_ds):
        assert splitted_ds == [dataset]


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('groupby', ['year'], indirect=True)
class TestByYear:

    def test_years(self, years):
        assert years == tuple(conftest.year_line)

    def test_splitted_datasets(self, splitted_ds):
        assert len(splitted_ds) == len(conftest.year_line)


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('groupby', ['decade'], indirect=True)
class TestByDecade:

    def test_years(self, years):
        assert years == tuple(y for y in conftest.year_line if y % 10 == 0)

    def test_splitted_datasets(self, splitted_ds):
        decades = [y for y in conftest.year_line if y % 10 == 0]
        assert len(splitted_ds) == len(decades)


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('groupby', ['unknown'], indirect=True)
class TestExceptions:

    def test_BadGroup(self, dataset, groupby):
        pytest.raises(KeyError, o3skim.group, dataset, groupby)
