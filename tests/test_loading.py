"""Pytest module to test sources as blackbox."""
import pytest
import tests.conftest as conftest

configs = conftest.available_configurations
models = conftest.available_models


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
class TestTCO3Load:

    @pytest.mark.parametrize('model', models['with_tco3'], indirect=True)
    def test_variable_load(self, dataset):
        assert 'tco3_zm' in dataset
        assert 'time' in dataset['tco3_zm'].coords
        assert 'lat' in dataset['tco3_zm'].coords
        assert 'lon' in dataset['tco3_zm'].coords
        assert len(dataset['tco3_zm'].coords) == 3

    @pytest.mark.parametrize('model', models['with_tco3'], indirect=True)
    def test_coordinates(self, dataset):
        assert 'time' in dataset.coords
        assert 'lat' in dataset.coords
        assert 'lon' in dataset.coords

    @pytest.mark.parametrize('model', models['only_tco3'], indirect=True)
    def test_no_extra_coordinates(self, dataset):
        assert len(dataset.coords) == 3


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
class TestVMRO3Load:

    @pytest.mark.parametrize('model', models['with_vmro3'], indirect=True)
    def test_variable_load(self, dataset):
        assert 'vmro3_zm' in dataset
        assert 'time' in dataset['vmro3_zm'].coords
        assert 'plev' in dataset['vmro3_zm'].coords
        assert 'lat' in dataset['vmro3_zm'].coords
        assert 'lon' in dataset['vmro3_zm'].coords
        assert len(dataset['vmro3_zm'].coords) == 4

    @pytest.mark.parametrize('model', models['with_vmro3'], indirect=True)
    def test_coordinates(self, dataset):
        assert 'time' in dataset.coords
        assert 'plev' in dataset.coords
        assert 'lat' in dataset.coords
        assert 'lon' in dataset.coords

    @pytest.mark.parametrize('model', models['only_vmro3'], indirect=True)
    def test_no_extra_coordinates(self, dataset):
        assert len(dataset.coords) == 4
