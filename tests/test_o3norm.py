"""Pytest module to test sources as blackbox."""
from o3skim.scripts import norm
import pytest
import xarray as xr


sources = {'CCMI-1', 'ECMWF', 'ESACCI', 'SBUV'}


@pytest.fixture()
def args(target, variable, source, s_args):
    args = ['-t', target, f"--{variable}", source, *s_args]
    return norm.parser.parse_args(args)


@pytest.fixture()
def s_args(source, variable, source_files):
    if source == 'CCMI-1':
        if variable == 'tco3_zm':
            return ['toz', *source_files]
        elif variable == 'vmro3_zm':
            return ['vmro3', *source_files]
        else:
            pytest.skip(f"This model does not support {variable}")
    if source == 'ECMWF':
        if variable == 'tco3_zm':
            return ['tco3', *source_files]
        elif variable == 'vmro3_zm':
            return ['vmro3', *source_files]
        else:
            pytest.skip(f"This model does not support {variable}")
    if source == 'ESACCI':
        if variable == 'tco3_zm':
            return ['atmosphere_mole_content_of_ozone', *source_files]
        else:
            pytest.skip(f"This model does not support {variable}")
    if source == 'SBUV':
        if variable == 'tco3_zm':
            return source_files
        else:
            pytest.skip(f"This model does not support {variable}")


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
