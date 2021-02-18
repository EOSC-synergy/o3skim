"""Pytest module to test sources as blackbox."""
import o3skim
import pytest
import tests.conftest as conftest
import xarray as xr

from o3skim.scripts import o3norm

sources = conftest.sources
models = conftest.models


@pytest.fixture()
def args(target, variable, source, s_args):
    parser = o3norm.parser()
    variable = '--' + variable
    return parser.parse_args(['-t', target, variable, source, *s_args])


@pytest.fixture()
def s_args(source, data_dir):
    if source == 'ccmi':
        return ['toz', data_dir + '/*.nc']
    if source == 'ecmwf':
        return ['tco3', data_dir + '/tco3_????.nc']


@pytest.fixture()
def dataset(setup_data, target, args):
    o3norm.run_command(**vars(args))
    return xr.open_dataset(target + '.nc')


@pytest.mark.parametrize('source', {'ccmi', 'ecmwf'}, indirect=True)
@pytest.mark.parametrize('variable', {'tco3_zm', 'vmro3_zm'}, indirect=True)
class TestsCommon:

    def test_simple(self, dataset):
        assert 'time' in dataset.coords

