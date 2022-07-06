"""Simple test module for testing"""
from glob import glob
from os import listdir

from o3skim.attributes import global_attributes
from o3skim.load_tco3 import ccmi, ecmwf, esacci, sbuv
from pytest import fixture, mark, skip


# Module fixtures ---------------------------------------------------
@fixture(scope="class", params=[])
def source(request):
    return request.param


@fixture(scope="class", params=[])
def model(request):
    return request.param


@fixture(scope="class", autouse=True)
def files(request, source, model):
    if glob(request.cls.path.format(source, model)) == []:
        skip(f"No dataset {source}/{model}")


# Requirements ------------------------------------------------------
class AttrRequirements:
    def test_variable(self, dataset):
        assert "tco3" in set(dataset.variables)
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


# Parametrization ---------------------------------------------------
@mark.parametrize("source", ["CCMI-1"], indirect=True)
@mark.parametrize("model", listdir("tests/datasets/CCMI-1"), indirect=True)
class TestCCMI(AttrRequirements):
    path = "tests/datasets/{}/{}/toz*.nc"

    @fixture(scope="class")
    def dataset(self, source, model):
        return ccmi(self.path.format(source, model))


@mark.parametrize("source", ["ECMWF"], indirect=True)
@mark.parametrize("model", listdir("tests/datasets/ECMWF"), indirect=True)
class TestECMWF(AttrRequirements):
    path = "tests/datasets/{}/{}/*.nc"

    @fixture(scope="class")
    def dataset(self, source, model):
        return ecmwf(self.path.format(source, model))


@mark.parametrize("source", ["ESACCI"], indirect=True)
@mark.parametrize("model", listdir("tests/datasets/ESACCI"), indirect=True)
class TestESACCI(AttrRequirements):
    path = "tests/datasets/{}/{}/*.nc"

    @fixture(scope="class")
    def dataset(self, source, model):
        return esacci(self.path.format(source, model))


@mark.parametrize("source", ["SBUV"], indirect=True)
@mark.parametrize("model", listdir("tests/datasets/SBUV"), indirect=True)
class TestSBUV(AttrRequirements):
    path = "tests/datasets/{}/{}/*.za.txt"

    @fixture(scope="class")
    def dataset(self, source, model):
        return sbuv(self.path.format(source, model))
