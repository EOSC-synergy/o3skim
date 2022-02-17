"""Simple test module for testing"""
import numpy as np
from pytest import mark

from . import Skimmed


class CommonTests(Skimmed):
    def test_toz_var_attrs(self, skimmed):
        assert skimmed.name() == "atmosphere_mole_content_of_ozone"
        assert str(skimmed.units) == "mol m-2"


@mark.parametrize("operation", ["year_mean"], indirect=True)
class TestYearMean(CommonTests):
    def test_1date_per_year(self, skimmed):
        diff_time = np.diff(skimmed.coord("time").bounds, 1)[:, 0]
        assert np.all(x >= 365 for x in diff_time)

    def test_coords_reduction(self, dataset, skimmed):
        assert dataset.ndim == skimmed.ndim

    def test_cell_methods(self, skimmed):
        assert skimmed.cell_methods[-1].method == "mean"
        assert skimmed.cell_methods[-1].coord_names == ("time",)
        assert skimmed.cell_methods[-1].intervals == ("1 year",)


@mark.parametrize("operation", ["lat_mean"], indirect=True)
class TestLatMean(CommonTests):
    def test_no_latitude(self, skimmed):
        assert "latitude" not in [x.name() for x in skimmed.dim_coords]

    def test_coords_reduction(self, dataset, skimmed):
        assert dataset.ndim == skimmed.ndim + 1

    def test_cell_methods(self, skimmed):
        assert skimmed.cell_methods[-1].method == "mean"
        assert skimmed.cell_methods[-1].coord_names == ("latitude",)
        assert skimmed.cell_methods[-1].intervals == ()


@mark.parametrize("operation", ["lon_mean"], indirect=True)
class TestLonMean(CommonTests):
    def test_no_longitude(self, skimmed):
        assert "longitude" not in [x.name() for x in skimmed.dim_coords]

    def test_coords_reduction(self, dataset, skimmed):
        assert dataset.ndim == skimmed.ndim + 1

    def test_cell_methods(self, skimmed):
        assert skimmed.cell_methods[-1].method == "mean"
        assert skimmed.cell_methods[-1].coord_names == ("longitude",)
        assert skimmed.cell_methods[-1].intervals == ()
