from o3skim import utils
from pytest import fixture, mark


@fixture(scope="class")
def dataset(dataset_gen):
    dataset = dataset_gen()
    dataset["atmosphere_mole_content_of_ozone"].attrs["non_standard"] = True
    dataset.attrs["non_standard"] = True
    dataset["time"].attrs["non_standard"] = True
    dataset["latitude"].attrs["non_standard"] = True
    dataset["longitude"].attrs["non_standard"] = True
    return dataset


class TestCleanGlobal:
    @fixture(scope="class", autouse=True)
    def clean_attributes(self, dataset):
        utils.cf_clean(dataset)

    def test_rm_non_standard(self, dataset):
        assert "non_standard" not in dataset.attrs

    def test_keep_Conventions(self, dataset):
        assert "Conventions" in dataset.attrs

    def test_keep_title(self, dataset):
        assert "title" in dataset.attrs

    def test_keep_references(self, dataset):
        assert "references" in dataset.attrs

    def test_keep_comment(self, dataset):
        assert "comment" in dataset.attrs


@mark.parametrize("coord", ["time", "longitude", "latitude"])
class TestCleanCoordinates:
    @fixture(scope="class", autouse=True)
    def clean_attributes(self, dataset):
        utils.cf_clean(dataset)

    def test_rm_non_standard(self, dataset, coord):
        assert "non_standard" not in dataset[coord].attrs

    def test_keep_std_name(self, dataset, coord):
        assert "standard_name" in dataset[coord].attrs

    def test_keep_long_name(self, dataset, coord):
        assert "long_name" in dataset[coord].attrs

    def test_keep_axis(self, dataset, coord):
        assert "axis" in dataset[coord].attrs


@mark.parametrize("var", ["atmosphere_mole_content_of_ozone"])
class TestCleanVariables:
    @fixture(scope="class", autouse=True)
    def clean_attributes(self, dataset):
        utils.cf_clean(dataset)

    def test_rm_non_standard(self, dataset, var):
        assert "non_standard" not in dataset[var].attrs

    def test_keep_std_name(self, dataset, var):
        assert "standard_name" in dataset[var].attrs

    def test_keep_long_name(self, dataset, var):
        assert "long_name" in dataset[var].attrs

    def test_keep_units(self, dataset, var):
        assert "units" in dataset[var].attrs
