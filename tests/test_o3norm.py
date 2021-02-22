"""Pytest module to test sources as blackbox."""
import pytest
import xarray as xr

from o3skim.scripts import o3norm
sources = {'ccmi', 'ecmwf', 'esacci', 'sbuv'}
var_names = {
    'ccmi':  dict(tco3_zm='toz', vmro3_zm='vmro3'),
    'ecmwf': dict(tco3_zm='tco3', vmro3_zm='vmro3'),
    'esacci': dict(tco3_zm='tco3', vmro3_zm='vmro3')}


@pytest.fixture()
def args(target, variable, source, s_args):
    if source == 'sbuv' and variable == 'vmro3_zm':
        pytest.skip('This model does not support vmro3')
    parser = o3norm.run_parser()
    variable = '--' + variable
    return parser.parse_args(['-t', target, variable, source, *s_args])


@pytest.fixture()
def s_args(source, variable, paths):
    if source == 'ccmi':
        return [var_names[source][variable]] + paths
    if source == 'ecmwf':
        return [var_names[source][variable]] + paths
    if source == 'esacci':
        return [var_names[source][variable]] + paths
    if source == 'sbuv':
        return paths


@pytest.fixture()
def dataset(target, args):
    o3norm.run_command(**vars(args))
    return xr.open_dataset(target + '.nc')


@pytest.mark.parametrize('variable', {'tco3_zm', 'vmro3_zm'}, indirect=True)
@pytest.mark.parametrize('source', sources, indirect=True)
class TestsCommon:

    # @pytest.mark.xfail(raises=NotImplementedError)
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

    # @pytest.mark.xfail(raises=NotImplementedError)
    def test_coordinates(self, dataset):
        assert 'plev' in dataset.coords
        assert len(dataset.coords) == 4
