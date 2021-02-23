"""Pytest module to test sources as blackbox."""
import pytest
import xarray as xr


@ pytest.fixture()
def dataset(o3data_files):
    return xr.open_mfdataset(o3data_files)


@pytest.mark.parametrize('split_by', {None, 'year', 'decade'}, indirect=True)
class TestsSavedDataset:

    def test_variables(self, dataset):
        assert 'tco3_zm' in dataset.var()
        assert 'vmro3_zm' in dataset.var()

    def test_coordinates(self, dataset):
        assert 'time' in dataset.coords
        assert 'plev' in dataset.coords
        assert 'lon' in dataset.coords
        assert 'lat' in dataset.coords

    def test_attrs(self, dataset):
        assert dataset.attrs == dict(description="Test ozone dataset")
