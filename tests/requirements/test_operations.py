"""Simple test module for testing"""
import cf_xarray as cfxr
import numpy as np
from pytest import fixture, mark
from tests.utils import all_perm

from . import Skimmed


class CommonTests(Skimmed):
    def test_toz_var_attrs(self, dataset, skimmed, operations):
        var = skimmed.cf["atmosphere_mole_content_of_ozone"]
        assert var.attrs["units"] == "mol m-2"
        assert "area: mean" in var.cell_methods
        if "year_mean" in operations:
            assert "time: mean (interval: 1 years)" in var.cell_methods


@mark.parametrize("operation", ["year_mean"], indirect=True)
@mark.parametrize("extra", all_perm("lat_mean", "lon_mean"), indirect=True)
class TestYearMean(CommonTests):
    def test_1date_per_year(self, skimmed):
        diff_time = skimmed.time.diff("time").values[:]
        assert np.all(diff_time.astype("timedelta64[D]") > np.timedelta64(364, "D"))
        assert np.all(diff_time.astype("timedelta64[D]") < np.timedelta64(367, "D"))

    @mark.parametrize("variable", ["atmosphere_mole_content_of_ozone"])
    def test_dim_reduction(self, dataset, skimmed, operations, variable):
        dataset_var = dataset.cf[variable]
        skimmed_var = skimmed.cf[variable]
        assert dataset_var.ndim == skimmed_var.ndim + len(operations) - 1

    def test_time_boundaries(self, skimmed):
        pass


@mark.parametrize("operation", ["lat_mean"], indirect=True)
@mark.parametrize("extra", all_perm("year_mean", "lon_mean"), indirect=True)
class TestLatMean(CommonTests):
    def test_no_latitude(self, skimmed):
        assert not "Y" in skimmed.cf

    @mark.parametrize("variable", ["atmosphere_mole_content_of_ozone"])
    def test_dim_reduction(self, dataset, skimmed, operations, variable):
        dataset_var = dataset.cf[variable]
        skimmed_var = skimmed.cf[variable]
        if "year_mean" in operations:
            assert dataset_var.ndim == skimmed_var.ndim + len(operations) - 1
        else:
            assert dataset_var.ndim == skimmed_var.ndim + len(operations)

    def test_lat_boundaries(self, skimmed):
        pass


@mark.parametrize("operation", ["lon_mean"], indirect=True)
@mark.parametrize("extra", all_perm("lat_mean", "year_mean"), indirect=True)
class TestLonMean(CommonTests):
    def test_no_longitude(self, skimmed):
        assert not "X" in skimmed.cf

    @mark.parametrize("variable", ["atmosphere_mole_content_of_ozone"])
    def test_dim_reduction(self, dataset, skimmed, operations, variable):
        dataset_var = dataset.cf[variable]
        skimmed_var = skimmed.cf[variable]
        if "year_mean" in operations:
            assert dataset_var.ndim == skimmed_var.ndim + len(operations) - 1
        else:
            assert dataset_var.ndim == skimmed_var.ndim + len(operations)

    def test_lon_boundaries(self, skimmed):
        pass
