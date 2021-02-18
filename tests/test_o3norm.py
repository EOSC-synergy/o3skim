"""Pytest module to test sources as blackbox."""
import o3skim
import pytest
import tests.conftest as conftest
import xarray as xr

from o3skim.scripts import o3norm


@pytest.fixture()
def args(target, variable, source, s_args):
    parser = o3norm.parser()
    variable = '--' + variable
    return parser.parse_args(['-t', target, variable, source, *s_args])


@pytest.fixture()
def s_args(var_name, paths):
    return [var_name] + paths


@pytest.fixture()
def dataset(target, args):
    o3norm.run_command(**vars(args))
    return xr.open_dataset(target + '.nc')


@pytest.mark.parametrize('variable', {'tco3_zm', 'vmro3_zm'}, indirect=True)
@pytest.mark.parametrize('source', {'ccmi', 'ecmwf'}, indirect=True)
class TestsCommon:

    def test_coordinates(self, dataset):
        assert 'time' in dataset.coords
        assert 'lon' in dataset.coords
        assert 'lat' in dataset.coords


@pytest.mark.parametrize('variable', {'tco3_zm'}, indirect=True)
@pytest.mark.parametrize('source', {'ccmi', 'ecmwf'}, indirect=True)
class TestsTCO3:

    def test_coordinates(self, dataset):
        assert len(dataset.coords) == 3


@pytest.mark.parametrize('variable', {'vmro3_zm'}, indirect=True)
@pytest.mark.parametrize('source', {'ccmi', 'ecmwf'}, indirect=True)
class TestsVMRO3:

    def test_coordinates(self, dataset):
        assert 'plev' in dataset.coords
        assert len(dataset.coords) == 4
