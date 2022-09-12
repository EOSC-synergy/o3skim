"""Simple test module for testing"""
import o3skim
from pytest import fixture, mark

VAR = "atmosphere_mole_content_of_ozone"


# Module fixtures ---------------------------------------------------
@fixture(scope="class", params=["standard", "with_methods", "no_bounds"])
def dataset(request, dataset_gen):
    dataset = dataset_gen()
    if request.param == "no_methods":
        del dataset[VAR].attrs["cell_methods"]
    if request.param == "no_bounds":
        dataset = dataset.drop_vars(["time_bounds"])
        del dataset["time"].attrs["bounds"]
        dataset = dataset.drop_vars(["longitude_bounds"])
        del dataset["longitude"].attrs["bounds"]
        dataset = dataset.drop_vars(["latitude_bounds"])
        del dataset["latitude"].attrs["bounds"]
    return dataset


@fixture(scope="class")
def bounds(dataset):
    bounds = [dataset[v].attrs.get("bounds", None) for v in dataset.coords]
    return set(bound for bound in bounds if bound is not None)


# Requirements ------------------------------------------------------
class VariableRequirements:
    @mark.parametrize("dataset", ["no_methods"], indirect=True)
    def test_var_attrs(self, dataset, skimmed):
        assert dataset.cf[VAR].attrs == skimmed.cf[VAR].attrs

    def test_global_attrs(self, dataset, skimmed):
        assert dataset.attrs == skimmed.attrs


class LatSkimRequirements:
    def test_variable_name(self, skimmed, dataset, bounds):
        for variable in skimmed.data_vars:
            assert skimmed[variable].name[:] in dataset
            assert True  # TODO: Requirement for lat zm?

    def test_boundary_names(self, skimmed, bounds):
        assert all(bound in skimmed for bound in bounds - {"latitude_bounds"})

    def test_no_latitude(self, skimmed):
        assert "latitude" not in skimmed.cf.coordinates

    @mark.parametrize("dataset", ["standard", "no_methods"], indirect=True)
    def test_no_lat_bounds(self, skimmed, dataset):
        assert dataset.cf["latitude"].attrs["bounds"] not in skimmed

    @mark.parametrize("dataset", ["standard", "no_bounds"], indirect=True)
    def test_cell_methods(self, skimmed):
        assert "latitude: mean" in skimmed.cf[VAR].attrs["cell_methods"]


class LonSkimRequirements:
    def test_variable_names(self, skimmed, dataset, bounds):
        for variable in set(skimmed.data_vars) - bounds:
            assert skimmed[variable].name[:-3] in dataset
            assert skimmed[variable].name[-3:] == "_zm"

    def test_boundary_names(self, skimmed, bounds):
        assert all(bound in skimmed for bound in bounds - {"longitude_bounds"})

    def test_no_longitude(self, skimmed):
        assert "longitude" not in skimmed.cf.coordinates

    @mark.parametrize("dataset", ["standard", "no_methods"], indirect=True)
    def test_no_lon_bounds(self, skimmed, dataset):
        assert dataset.cf["longitude"].attrs["bounds"] not in skimmed

    @mark.parametrize("dataset", ["standard", "no_bounds"], indirect=True)
    def test_cell_methods(self, skimmed):
        assert "longitude: mean" in skimmed.cf[VAR].attrs["cell_methods"]


# Parametrization ---------------------------------------------------
class TestLatMean(VariableRequirements, LatSkimRequirements):
    @fixture(scope="class", autouse=True)
    def skimmed(self, dataset):
        return o3skim.lat_mean(dataset)


class TestLonMean(VariableRequirements, LonSkimRequirements):
    @fixture(scope="class", autouse=True)
    def skimmed(self, dataset):
        return o3skim.lon_mean(dataset)
