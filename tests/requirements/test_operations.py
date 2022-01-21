"""Simple test module for testing"""
import numpy as np
from pytest import mark

from . import Skimmed


class CommonTests(Skimmed):
    def test_toz_var_attrs(self, skimmed):
        assert skimmed.name() == "atmosphere_mole_content_of_ozone"
        assert str(skimmed.units) == "mol m-2"

    def cell_methods(self, cube):
        return [f"{x.coord_names[0]}: {x.method}" for x in cube.cell_methods]


@mark.parametrize("operation", ["year_mean"], indirect=True)
class TestYearMean(CommonTests):
    def test_1date_per_year(self, skimmed):
        diff_time = np.diff(skimmed.coord("time").bounds, 1)[:, 0]
        assert np.all(x >= 365 for x in diff_time)

    @mark.skip(reason="TODO")
    def test_time_boundaries(self, skimmed):
        pass  # TODO

    def test_coords_reduction(self, dataset, skimmed):
        assert dataset.ndim == skimmed.ndim

    def test_cell_methods(self, skimmed):
        assert "year: mean" in self.cell_methods(skimmed)


@mark.parametrize("operation", ["lat_mean"], indirect=True)
class TestLatMean(CommonTests):
    def test_no_latitude(self, skimmed):
        assert "latitude" not in [x.name() for x in skimmed.dim_coords]

    @mark.skip(reason="TODO")
    def test_lat_boundaries(self, skimmed):
        pass  # TODO

    def test_coords_reduction(self, dataset, skimmed):
        assert dataset.ndim == skimmed.ndim + 1

    def test_cell_methods(self, skimmed):
        assert "latitude: mean" in self.cell_methods(skimmed)


@mark.parametrize("operation", ["lon_mean"], indirect=True)
class TestLonMean(CommonTests):
    def test_no_longitude(self, skimmed):
        assert "longitude" not in [x.name() for x in skimmed.dim_coords]

    @mark.skip(reason="TODO")
    def test_lon_boundaries(self, skimmed):
        pass  # TODO

    def test_coords_reduction(self, dataset, skimmed):
        assert dataset.ndim == skimmed.ndim + 1

    def test_cell_methods(self, skimmed):
        assert "longitude: mean" in self.cell_methods(skimmed)
