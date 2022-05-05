import numpy as np
import pandas as pd
import xarray as xr
from o3skim import utils
from pytest import fixture, mark


# Module fixtures ---------------------------------------------------
@fixture(scope="class")
def dataset():
    return xr.Dataset(
        data_vars=dict(
            temperature=xr.Variable(
                ["x", "y", "time"],
                15 + 8 * np.random.randn(2, 2, 3),
                attrs=dict(
                    units="K",
                    long_name="Air temperature",
                    standard_name="air_temperature",
                ),
            ),
            precipitation=xr.Variable(
                ["x", "y", "time"],
                10 * np.random.rand(2, 2, 3),
                attrs=dict(
                    units="kg m-2",
                    long_name="Amount means mass per unit area.",
                    standard_name="precipitation_amount",
                ),
            ),
        ),
        coords=dict(
            lon=xr.Variable(
                ["x", "y"],
                [[-99.83, -99.32], [-99.79, -99.23]],
                attrs=dict(
                    units="degrees_east",
                    long_name="Longitude of the grid center",
                    axis="X",
                    standard_name="longitude",
                    valid_range=np.array([0.0, 360.0]),
                ),
            ),
            lat=xr.Variable(
                ["x", "y"],
                [[42.25, 42.21], [42.63, 42.59]],
                attrs=dict(
                    units="degrees_north",
                    long_name="Latitude of the grid center",
                    axis="Y",
                    standard_name="latitude",
                    valid_range=np.array([-90.0, 90.0]),
                ),
            ),
            time=xr.Variable(
                ["time"],
                pd.date_range("2014-09-06", periods=3),
                attrs=dict(
                    long_name="time",
                    axis="T",
                    standard_name="time",
                ),
            ),
            reference_time=pd.Timestamp("2014-09-05"),
        ),
        attrs=dict(
            Conventions="CF-1.5",
            title="NetCDF CF file prov...servations",
            references="GTO-ECV reference: L...318, 2009.",
            comment="Product generated at...I project.",
            non_standard=True,
        ),
    )


# Requirements ------------------------------------------------------
class ReqGlobalCF:
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


class ReqCoordsCF:
    def test_rm_non_standard(self, dataset, coord):
        assert "non_standard" not in dataset[coord].attrs

    def test_keep_std_name(self, dataset, coord):
        assert "standard_name" in dataset[coord].attrs

    def test_keep_long_name(self, dataset, coord):
        assert "long_name" in dataset[coord].attrs

    def test_keep_axis(self, dataset, coord):
        assert "axis" in dataset[coord].attrs


class ReqVarsCF:
    def test_rm_non_standard(self, dataset, var):
        assert "non_standard" not in dataset[var].attrs

    def test_keep_std_name(self, dataset, var):
        assert "standard_name" in dataset[var].attrs

    def test_keep_long_name(self, dataset, var):
        assert "long_name" in dataset[var].attrs

    def test_keep_units(self, dataset, var):
        assert "units" in dataset[var].attrs


# Parametrization ---------------------------------------------------
class TestCleanGlobal(ReqGlobalCF):
    @fixture(scope="class", autouse=True)
    def clean_attributes(self, dataset):
        utils.cf_clean(dataset)


@mark.parametrize("coord", ["time", "lon", "lat"])
class TestCleanCoordinates(ReqCoordsCF):
    @fixture(scope="class", autouse=True)
    def clean_attributes(self, dataset):
        utils.cf_clean(dataset)


@mark.parametrize("var", ["temperature", "precipitation"])
class TestCleanVariables(ReqVarsCF):
    @fixture(scope="class", autouse=True)
    def clean_attributes(self, dataset):
        utils.cf_clean(dataset)
