"""Fixtures module for pytest"""
import numpy as np
import pandas as pd
import xarray as xr
from pytest import fixture


@fixture(scope="class")
def dataset_gen():
    return lambda: xr.Dataset(
        data_vars=dict(
            atmosphere_mole_content_of_ozone=xr.Variable(
                ["longitude", "latitude", "time"],
                15 + 8 * np.random.randn(2, 2, 3),
                attrs=dict(
                    units="mol m-2",
                    long_name="Total column of ozone in the atmosphere",
                    standard_name="atmosphere_mole_content_of_ozone",
                    cell_methods="area: max",
                ),
            ),
            longitude_bounds=xr.Variable(
                ["longitude", "bounds"],
                [(0, 180), (180, 360)],
            ),
            latitude_bounds=xr.Variable(
                ["latitude", "bounds"],
                [(-90, 0), (0, 90)],
            ),
            time_bounds=xr.Variable(
                ["time", "bounds"],
                list(
                    zip(
                        pd.date_range("2014-09-06", periods=3),
                        pd.date_range("2014-09-07", periods=3),
                    )
                ),
            ),
        ),
        coords=dict(
            longitude=xr.Variable(
                ["longitude"],
                [90, 270],
                attrs=dict(
                    standard_name="longitude",
                    axis="X",
                    units="degrees_east",
                    long_name="Longitude of the grid center",
                    bounds="longitude_bounds",
                    valid_range=np.array([0.0, 360.0]),
                ),
            ),
            latitude=xr.Variable(
                ["latitude"],
                [-45, 45],
                attrs=dict(
                    units="degrees_north",
                    long_name="Latitude of the grid center",
                    axis="Y",
                    standard_name="latitude",
                    bounds="latitude_bounds",
                    valid_range=np.array([-90.0, 90.0]),
                ),
            ),
            time=xr.Variable(
                ["time"],
                pd.date_range("2014-09-06", periods=3),
                attrs=dict(
                    standard_name="time",
                    axis="T",
                    long_name="time",
                    bounds="time_bounds",
                ),
            ),
            bounds=xr.Variable(["bounds"], [0, 1]),
            reference_time=pd.Timestamp("2014-09-05"),
        ),
        attrs=dict(
            Conventions="CF-1.5",
            title="NetCDF CF file prov...servations",
            references="GTO-ECV reference: L...318, 2009.",
            comment="Product generated at...I project.",
        ),
    )
