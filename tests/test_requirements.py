"""Simple test module for testing"""
from pytest import fixture, mark
import numpy as np


from tests.utils import all_perm
from . import Skimmed


@mark.parametrize("operation", ["year_mean"], indirect=True)
@mark.parametrize("extra", all_perm("lat_mean", "lon_mean"), indirect=True)
class TestYearMean(Skimmed):
    def test_1date_per_year(self, dataset, skimmed):
        diff_time = skimmed.time.diff("time").values[:]
        assert np.all(diff_time.astype("timedelta64[D]") > np.timedelta64(364, "D"))
        assert np.all(diff_time.astype("timedelta64[D]") < np.timedelta64(367, "D"))

    def test_dim_reduction(self, dataset, skimmed, operations):
        for var in dataset.var():
            assert dataset[var].ndim == skimmed[var].ndim + len(operations) - 1
