from numpy import var
from o3skim import utils
from pytest import mark


def test_cf_clean_global(dataset):
    original_attrs = dataset.attrs
    dataset.attrs = {"no_standard": True, **dataset.attrs}
    utils.cf_clean(dataset)
    assert "no_standard" not in dataset.attrs
    assert dataset.attrs == original_attrs


@mark.parametrize("coord", ["time"])
def test_cf_clean_coordinate(dataset, coord):
    original_attrs = dataset[coord].attrs
    dataset[coord].attrs = {"no_standard": True, **dataset[coord].attrs}
    utils.cf_clean(dataset)
    assert "no_standard" not in dataset[coord].attrs
    assert dataset[coord].attrs == original_attrs


def test_cf_clean_variable(dataset, variable):
    original_attrs = dataset.cf[variable].attrs
    dataset.cf[variable].attrs = {"no_standard": True, **dataset.cf[variable].attrs}
    utils.cf_clean(dataset)
    assert "no_standard" not in dataset.cf[variable].attrs
    assert dataset.cf[variable].attrs == original_attrs
