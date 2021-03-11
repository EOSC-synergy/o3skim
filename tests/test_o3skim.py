"""Pytest module to test sources as blackbox."""
import itertools
from o3skim.scripts import skim
from o3skim import operations as o3skim_operations
import pandas as pd
import pytest
import xarray as xr


operations = ['lon_mean', 'lat_mean', 'year_mean']
actions = list(itertools.permutations(operations))
using = {
    'any': [list(x) for x in actions],
    'lon_mean': [list(x) for x in actions if 'lon_mean' in x],
    'lat_mean': [list(x) for x in actions if 'lat_mean' in x],
    'year_mean': [list(x) for x in actions if 'year_mean' in x],
}


@pytest.fixture()
def args(operations, output, o3data_files):
    operations = ["--{}".format(x) for x in operations]
    args = [*operations, '-o', output, *o3data_files]
    return skim.parser.parse_args(args)


@pytest.fixture()
def original(o3data_files):
    return xr.open_mfdataset(o3data_files)


@pytest.fixture()
def processed(output, args):
    skim.run_command(**vars(args))
    return xr.open_mfdataset(f"{output}/*.nc")


@pytest.mark.parametrize('split_by', {None, 'year', 'decade'}, indirect=True)
@pytest.mark.parametrize('operations', using['any'], indirect=True)
class TestsCommon:

    def test_attrs(self, original, processed):
        assert original.attrs == processed.attrs
        for o3var in processed.var():
            assert original[o3var].attrs == processed[o3var].attrs


@pytest.mark.parametrize('split_by', {None, 'year', 'decade'}, indirect=True)
class TestLonMean:

    @pytest.mark.parametrize('operations', using['lon_mean'], indirect=True)
    def test_coord_lon(self, processed):
        assert 'lon' not in processed.coords

    @pytest.mark.parametrize('operations', [['lon_mean']], indirect=True)
    def test_coordinates(self, original, processed):
        assert len(original.coords) == len(processed.coords) + 1


@pytest.mark.parametrize('split_by', {None, 'year', 'decade'}, indirect=True)
class TestLatMean:

    @pytest.mark.parametrize('operations', using['lat_mean'], indirect=True)
    def test_coord_lat(self, processed):
        assert 'lat' not in processed.coords

    @pytest.mark.parametrize('operations', [['lat_mean']], indirect=True)
    def test_coordinates(self, original, processed):
        assert len(original.coords) == len(processed.coords) + 1


@pytest.mark.parametrize('split_by', {None, 'year', 'decade'}, indirect=True)
class TestYearMean:

    @pytest.mark.parametrize('operations', using['year_mean'], indirect=True)
    def test_no_repeated_years(self, processed):
        years = [pd.to_datetime(x.values).year for x in processed.time]
        assert len(set(years)) == len(processed.time)

    @pytest.mark.parametrize('operations', [['year_mean']], indirect=True)
    def test_coordinates(self, original, processed):
        assert len(original.coords) == len(processed.coords)


@pytest.mark.parametrize('split_by', {None}, indirect=True)
class TestExceptions:

    @pytest.mark.parametrize('operation', {'wrong_operation'})
    def test_badOperation(self, operation, original):
        with pytest.raises(KeyError) as excinfo:
            o3skim_operations.run(operation, original)
        assert "Bad selected operation" in str(excinfo.value)
