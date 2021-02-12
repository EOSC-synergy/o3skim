"""Pytest module to test sources as blackbox."""
import itertools
import pytest
import tests.conftest as conftest

configs = conftest.available_configurations
models = conftest.available_models

operations = ['lon_mean', 'lat_mean']
actions = list(itertools.permutations(operations))
using = {
    'any': [list(x) for x in actions],
    'lon_mean': [list(x) for x in actions if 'lon_mean' in x],
    'lat_mean': [list(x) for x in actions if 'lat_mean' in x]
}


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('actions', using['any'], indirect=True)
class TestCommon:

    def test_attrs(self, dataset, processed):
        assert dataset.attrs == processed.attrs
        for o3var in processed.var():
            assert dataset[o3var].attrs == processed[o3var].attrs


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
class TestLonMean:

    @pytest.mark.parametrize('actions', using['lon_mean'], indirect=True)
    def test_coord_lon(self, processed):
        assert 'lon' not in processed.coords

    @pytest.mark.parametrize('actions', [['lon_mean']], indirect=True)
    def test_coordinates(self, dataset, processed):
        assert len(dataset.coords) == len(processed.coords) + 1


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
class TestLatMean:

    @pytest.mark.parametrize('actions', using['lat_mean'], indirect=True)
    def test_coord_lat(self, processed):
        assert 'lat' not in processed.coords

    @pytest.mark.parametrize('actions', [['lat_mean']], indirect=True)
    def test_coordinates(self, dataset, processed):
        assert len(dataset.coords) == len(processed.coords) + 1
