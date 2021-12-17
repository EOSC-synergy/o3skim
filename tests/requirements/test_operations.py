"""Simple test module for testing"""
import cf_xarray as cfxr
import numpy as np
from pytest import fixture, mark

from . import Skimmed


class CommonTests(Skimmed):
    def test_toz_var_attrs(self, skimmed):
        var = skimmed.cf["atmosphere_mole_content_of_ozone"]
        assert var.attrs["units"] == "mol m-2"
        assert "area: mean" in var.cell_methods


@mark.parametrize("operation", ["year_mean"], indirect=True)
class TestYearMean(CommonTests):
    def test_1date_per_year(self, skimmed):
        diff_time = skimmed.time.diff("time").values[:]
        assert np.all(diff_time.astype("timedelta64[D]") > np.timedelta64(364, "D"))
        assert np.all(diff_time.astype("timedelta64[D]") < np.timedelta64(367, "D"))

    @mark.skip(reason="TODO")
    def test_time_boundaries(self, skimmed):
        pass  # TODO

    def test_coords_reduction(self, dataset, skimmed):
        assert len(dataset.coords) == len(skimmed.coords)

    @mark.parametrize("variable", ["atmosphere_mole_content_of_ozone"])
    def test_cell_methods(self, skimmed, variable):
        var = skimmed.cf[variable]
        assert "time: mean (interval: 1 years)" in var.cell_methods


@mark.parametrize("operation", ["lat_mean"], indirect=True)
class TestLatMean(CommonTests):
    def test_no_latitude(self, skimmed):
        assert not "Y" in skimmed.cf

    @mark.skip(reason="TODO")
    def test_lat_boundaries(self, skimmed):
        pass  # TODO

    def test_coords_reduction(self, dataset, skimmed):
        assert len(dataset.coords) == len(skimmed.coords) + 1

    @mark.parametrize("variable", ["atmosphere_mole_content_of_ozone"])
    def test_cell_methods(self, skimmed, variable):
        var = skimmed.cf[variable]
        assert not "lat" in var.cell_methods


@mark.parametrize("operation", ["lon_mean"], indirect=True)
class TestLonMean(CommonTests):
    def test_no_longitude(self, skimmed):
        assert not "X" in skimmed.cf

    @mark.skip(reason="TODO")
    def test_lon_boundaries(self, skimmed):
        pass  # TODO

    def test_coords_reduction(self, dataset, skimmed):
        assert len(dataset.coords) == len(skimmed.coords) + 1

    @mark.parametrize("variable", ["atmosphere_mole_content_of_ozone"])
    def test_cell_methods(self, skimmed, variable):
        var = skimmed.cf[variable]
        assert not "lon" in var.cell_methods
