"""Pytest module to test sources as blackbox."""
import pytest
import tests.conftest as conftest

configs = conftest.available_configurations
models = conftest.available_models


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
class TestO3CommonsLoad:

    def test_attrs(self, dataset):
        assert dataset.attrs == dict(description="Test ozone dataset")

    def test_metadata(self, metadata):
        assert metadata["meta_1"] == "Model metadata string example"
        assert metadata["meta_2"]["meta_21"] == "Sub-metadata from Model"


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
class TestTCO3Load:

    @pytest.mark.parametrize('model', models['with_tco3'], indirect=True)
    def test_variable_load(self, dataset):
        assert 'tco3_zm' in dataset
        darray = dataset['tco3_zm']
        assert 'time' in darray.coords
        assert 'lat' in darray.coords
        assert 'lon' in darray.coords
        assert len(darray.coords) == 3
        assert darray.attrs == dict(description="Test tco3 xarray")

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
        darray = dataset['vmro3_zm']
        assert 'time' in darray.coords
        assert 'plev' in darray.coords
        assert 'lat' in darray.coords
        assert 'lon' in darray.coords
        assert len(darray.coords) == 4
        assert darray.attrs == dict(description="Test vmro3 xarray")

    @pytest.mark.parametrize('model', models['with_vmro3'], indirect=True)
    def test_coordinates(self, dataset):
        assert 'time' in dataset.coords
        assert 'plev' in dataset.coords
        assert 'lat' in dataset.coords
        assert 'lon' in dataset.coords

    @pytest.mark.parametrize('model', models['only_vmro3'], indirect=True)
    def test_no_extra_coordinates(self, dataset):
        assert len(dataset.coords) == 4
