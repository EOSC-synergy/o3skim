"""Pytest module to test sources as blackbox."""
import pytest
import xarray as xr

import o3skim
from tests.mockup import standard


@pytest.fixture()
def tco3_ds():
    dsx = [standard.random_tco3_dataset(y) for y in range(2000, 2022)]
    return xr.concat(dsx, dim='time')


@pytest.fixture()
def vmro3_ds():
    dsx = [standard.random_vmro3_dataset(y) for y in range(2000, 2022)]
    return xr.concat(dsx, dim='time')


@pytest.fixture(scope='session')
def split_by(request):
    return request.param


@ pytest.fixture()
def dataset(target, tco3_ds, vmro3_ds, split_by):
    o3skim.save(tco3_ds, target, split_by)
    o3skim.save(vmro3_ds, target, split_by)
    return xr.open_mfdataset(target + '*.nc')


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
