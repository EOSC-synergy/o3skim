"""Pytest module to test sources as blackbox."""
from o3skim.scripts import norm
import pytest
import xarray as xr


sources = {'ccmi', 'ecmwf', 'esacci', 'sbuv'}
var_names = {
    'ccmi':  dict(tco3_zm='toz', vmro3_zm='vmro3'),
    'ecmwf': dict(tco3_zm='tco3', vmro3_zm='vmro3'),
    'esacci': dict(tco3_zm='tco3', vmro3_zm='vmro3')}


@pytest.fixture()
def args(target, variable, source, s_args):
    if source == 'sbuv' and variable == 'vmro3_zm':
        pytest.skip('This model does not support vmro3')
    args = ['-t', target, f"--{variable}", source, *s_args]
    return norm.parser.parse_args(args)


@pytest.fixture()
def s_args(source, variable, source_files):
    if source == 'ccmi':
        return [var_names[source][variable]] + source_files
    if source == 'ecmwf':
        return [var_names[source][variable]] + source_files
    if source == 'esacci':
        return [var_names[source][variable]] + source_files
    if source == 'sbuv':
        return source_files


@pytest.fixture()
def dataset(target, args):
    norm.run_command(**vars(args))
    return xr.open_dataset(target + '.nc')


@pytest.mark.parametrize('variable', {'tco3_zm', 'vmro3_zm'}, indirect=True)
@pytest.mark.parametrize('source', sources, indirect=True)
class TestsCommon:

    def test_coordinates(self, dataset):
        assert 'time' in dataset.coords
        assert 'lon' in dataset.coords
        assert 'lat' in dataset.coords


@pytest.mark.parametrize('variable', {'tco3_zm'}, indirect=True)
@pytest.mark.parametrize('source', sources, indirect=True)
class TestsTCO3:

    def test_coordinates(self, dataset):
        assert len(dataset.coords) == 3


@pytest.mark.parametrize('variable', {'vmro3_zm'}, indirect=True)
@pytest.mark.parametrize('source', sources, indirect=True)
class TestsVMRO3:

    def test_coordinates(self, dataset):
        assert 'plev' in dataset.coords
        assert len(dataset.coords) == 4
