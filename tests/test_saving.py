"""Pytest module to test sources as blackbox."""
import os
import o3skim
import pytest
import tests.conftest as conftest
import xarray as xr

configs = conftest.available_configurations
models = conftest.available_models


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('groupby', [None, 'year', 'decade'], indirect=True)
class TestNetCDFSaving:

    def test_arefiles(self, output_cd, save_netCDF, expected_netCDF):
        assert set(os.listdir()) == set(expected_netCDF)

    def test_saved_data(self, dataset, saved_ds, variables):
        xr.testing.assert_equal(dataset, saved_ds)
        assert set(variables) == set(saved_ds.var())
        assert set(dataset.coords) == set(saved_ds.coords)

    def test_saved_attrs(self, dataset, saved_ds):
        assert dataset.attrs == saved_ds.attrs


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
class TestMetadataSaving:

    def test_isfile(self, metadata_cd, save_metadata):
        assert os.path.isfile("metadata.yaml")

    def test_content(self, metadata, metadata_file_content):
        assert metadata == metadata_file_content


@pytest.mark.parametrize('config', configs['correct'], indirect=True)
@pytest.mark.parametrize('model', models['all'], indirect=True)
@pytest.mark.parametrize('groupby', ['unknown'], indirect=True)
class TestExceptions:

    def test_BadGroup(self, output_cd, dataset, groupby):
        pytest.raises(KeyError, o3skim.saving, dataset, groupby)
