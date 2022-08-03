"""Simple test module for testing"""
from os import listdir

import o3skim
from o3skim import config
from o3skim.attributes import global_attributes
from pytest import fixture, mark


# Module fixtures ---------------------------------------------------
@fixture(scope="class", params=[])
def model(request):
    return request.param


# Requirements ------------------------------------------------------
class AttrRequirements:
    def test_variable(self, dataset):
        assert "tco3" in set(dataset.variables)
        assert dataset.tco3.standard_name == config.TCO3_STANDARD_NAME
        assert dataset.tco3.units == "DU"
        assert dataset.tco3.ndim == 3
        if dataset.cf.bounds:  # Bounds are variables
            assert len(dataset.cf.data_vars) <= 4
        else:
            assert len(dataset.cf.data_vars) == 1

    def test_coord_lat(self, dataset):
        assert "lat" in dataset.coords
        assert dataset["lat"].standard_name == "latitude"
        assert dataset["lat"].axis == "Y"
        assert dataset["lat"].units == "degrees_north"
        if "Y" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["Y"] == ["lat_bnds"]

    def test_coord_lon(self, dataset):
        assert "lon" in dataset.coords
        assert dataset["lon"].standard_name == "longitude"
        assert dataset["lon"].axis == "X"
        assert dataset["lon"].units == "degrees_east"
        if "X" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["X"] == ["lon_bnds"]

    def test_coord_time(self, dataset):
        assert "time" in dataset.coords
        assert dataset["time"].standard_name == "time"
        assert dataset["time"].axis == "T"
        if "T" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["T"] == ["time_bnds"]

    def test_attributes(self, dataset):
        assert all(k in global_attributes.index for k in dataset.attrs)
        assert "Conventions" in dataset.attrs
        assert "institution" in dataset.attrs
        assert "source" in dataset.attrs

    @mark.parametrize("coord", ["latitude", "longitude"])
    def test_operations(self, dataset, coord):
        try:
            dataset.cf.mean(coord)
        except Exception:
            assert False


# Parametrization ---------------------------------------------------
@mark.parametrize("model", listdir("tests/datasets_tco3"), indirect=True)
class TestTCO3LoadFunction(AttrRequirements):
    @fixture(scope="class")
    def dataset(self, model):
        return o3skim.load_tco3(f"tests/datasets_tco3/{model}/*", model)
