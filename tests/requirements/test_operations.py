"""Simple test module for testing"""
from pytest import mark


class VariableRequirements:
    def test_standard_name(self, standard_name):
        assert standard_name == "atmosphere_mole_content_of_ozone"

    def test_standard_unit(self, units):
        assert units == "mol m-2"


class LatSkimRequirements:
    def test_no_latitude(self, skimmed):
        assert "latitude" not in skimmed.cf.coordinates

    @mark.xfail(raises=KeyError)
    def test_no_lat_bounds(self, skimmed, dataset):
        assert dataset.cf["latitude"].attrs["bounds"] not in skimmed

    def test_cell_methods(self, cell_methods):
        assert " latitude: mean" in cell_methods


class LonSkimRequirements:
    def test_no_longitude(self, skimmed):
        assert "longitude" not in skimmed.cf.coordinates

    @mark.xfail(raises=KeyError)
    def test_no_lon_bounds(self, skimmed, dataset):
        assert dataset.cf["longitude"].attrs["bounds"] not in skimmed

    def test_cell_methods(self, cell_methods):
        assert " longitude: mean" in cell_methods


@mark.parametrize("operations", [["lat_mean"]], indirect=True)
class TestLatMean(VariableRequirements, LatSkimRequirements):
    pass


@mark.parametrize("operations", [["lon_mean"]], indirect=True)
class TestLonMean(VariableRequirements, LonSkimRequirements):
    pass
