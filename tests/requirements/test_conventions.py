"""Simple test module for testing"""
from os import listdir

from o3skim import loads
from o3skim.attributes import global_attributes
from pytest import fixture, mark


# Module fixtures ---------------------------------------------------
@fixture(scope="class", params=[])
def source(request):
    return request.param


# Requirements ------------------------------------------------------
class AttrRequirements:
    def test_variable(self, dataset):
        assert "tco3" in set(dataset.variables)
        if dataset.cf.bounds:  # Bounds are variables
            assert len(dataset.cf.data_vars) <= 4
        else:
            assert len(dataset.cf.data_vars) == 1

    def test_coordinates(self, dataset):
        assert set(dataset.coords) == {"time", "lat", "lon"}
        assert dataset["time"].standard_name == "time"
        assert dataset["lat"].standard_name == "latitude"
        assert dataset["lon"].standard_name == "longitude"

        if "T" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["T"] == ["time_bnds"]
        if "X" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["X"] == ["lon_bnds"]
        if "Y" in dataset.cf.bounds:  # Not required
            assert dataset.cf.bounds["Y"] == ["lat_bnds"]

    @mark.parametrize("attrs", [global_attributes().index])
    def test_attributes(self, dataset, attrs):
        assert all(k in attrs for k in dataset.attrs)
        assert "Conventions" in dataset.attrs
        assert "institution" in dataset.attrs
        assert "source" in dataset.attrs


# Parametrization ---------------------------------------------------
@mark.parametrize("source", ["CCMI-1"], indirect=True)
class TestCCMI(AttrRequirements):
    @fixture(scope="class", params=listdir("tests/datasets/CCMI-1"))
    def model(self, request):
        return request.param

    @fixture(scope="class")
    def dataset(self, source, model):
        return loads.ccmi(f"tests/datasets/{source}/{model}/*.nc")


@mark.parametrize("source", ["ECMWF"], indirect=True)
class TestECMWF(AttrRequirements):
    @fixture(scope="class", params=listdir("tests/datasets/ECMWF"))
    def model(self, request):
        return request.param

    @fixture(scope="class")
    def dataset(self, source, model):
        return loads.ecmwf(f"tests/datasets/{source}/{model}/*.nc")


@mark.parametrize("source", ["ESACCI"], indirect=True)
class TestESACCI(AttrRequirements):
    @fixture(scope="class", params=listdir("tests/datasets/ESACCI"))
    def model(self, request):
        return request.param

    @fixture(scope="class")
    def dataset(self, source, model):
        return loads.esacci(f"tests/datasets/{source}/{model}/*.nc")


@mark.parametrize("source", ["SBUV"], indirect=True)
class TestSBUV(AttrRequirements):
    @fixture(scope="class", params=listdir("tests/datasets/SBUV"))
    def model(self, request):
        return request.param

    @fixture(scope="class")
    def dataset(self, source, model):
        return loads.sbuv(f"tests/datasets/{source}/{model}/*.za.txt")
