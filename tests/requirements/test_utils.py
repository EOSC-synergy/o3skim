from o3skim import utils


def test_cf_clean_global(dataset):
    original_attrs = dataset.attrs
    dataset.attrs = {"no_standard": True, **dataset.attrs}
    utils.cf_clean(dataset)
    assert "no_standard" not in dataset.attrs
    assert dataset.attrs == original_attrs


def test_cf_clean_coordinate(dataset):
    original_attrs = dataset["time"].attrs
    dataset["time"].attrs = {"no_standard": True, **dataset["time"].attrs}
    utils.cf_clean(dataset)
    assert "no_standard" not in dataset["time"].attrs
    assert dataset["time"].attrs == original_attrs


def test_cf_clean_variable(dataset):
    original_attrs = dataset["toz_zm"].attrs
    dataset["toz_zm"].attrs = {"no_standard": True, **dataset["toz_zm"].attrs}
    utils.cf_clean(dataset)
    assert "no_standard" not in dataset["toz_zm"].attrs
    assert dataset["toz_zm"].attrs == original_attrs
