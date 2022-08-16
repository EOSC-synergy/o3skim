"""Simple test module for testing"""
from os import listdir

import o3skim
from o3skim.attributes import global_attributes
from o3skim.settings import TCO3_DATA_VARIABLE as DATA_VARIABLE
from o3skim.settings import TCO3_STANDARD_NAME as STANDARD_NAME
from o3skim.settings import TCO3_STANDARD_UNIT as STANDARD_UNIT
from pytest import fixture, mark


# Module fixtures ---------------------------------------------------
@fixture(scope="class", params=[])
def model(request):
    return request.param


# Requirements ------------------------------------------------------
class AttrRequirements:
    def test_variable(self, dataset):
        assert DATA_VARIABLE in set(dataset.variables)
        assert dataset[DATA_VARIABLE].dtype == "float32"
        assert dataset[DATA_VARIABLE].standard_name == STANDARD_NAME
        assert dataset[DATA_VARIABLE].units == STANDARD_UNIT
        assert dataset[DATA_VARIABLE].ndim == 3
        if dataset.cf.bounds:  # Bounds are variables
            assert len(dataset.cf.data_vars) <= 4
        else:
            assert len(dataset.cf.data_vars) == 1

    def test_coord_lat(self, dataset):
        assert "latitude" in dataset.cf.coords
        assert dataset.cf["latitude"].name == "lat"
        assert dataset.cf["latitude"].dtype == "float32"
        assert dataset.cf["latitude"].standard_name == "latitude"
        assert dataset.cf["latitude"].axis == "Y"
        assert dataset.cf["latitude"].units == "degrees_north"
        if "Y" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["Y"] == ["lat_bnds"]

    def test_coord_lon(self, dataset):
        assert "longitude" in dataset.cf.coords
        assert dataset.cf["longitude"].name == "lon"
        assert dataset.cf["longitude"].dtype == "float32"
        assert dataset.cf["longitude"].standard_name == "longitude"
        assert dataset.cf["longitude"].axis == "X"
        assert dataset.cf["longitude"].units == "degrees_east"
        if "X" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["X"] == ["lon_bnds"]

    def test_coord_plev(self, dataset):
        assert "air_pressure" not in dataset.cf.coords

    def test_coord_time(self, dataset):
        assert "time" in dataset.cf.coords
        assert dataset.cf["time"].name == "time"
        assert dataset.cf["time"].dtype == "<M8[ns]"
        assert dataset.cf["time"].standard_name == "time"
        assert dataset.cf["time"].axis == "T"
        if "T" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["T"] == ["time_bnds"]

    def test_attributes(self, dataset):
        assert all(k in global_attributes.index for k in dataset.attrs)
        assert "Conventions" in dataset.attrs
        assert "institution" in dataset.attrs
        assert "source" in dataset.attrs

    @mark.parametrize("coord", ["latitude", "longitude", "time"])
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
