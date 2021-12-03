"""Mockup module to produce CF-1.9 data"""
import datetime

import cftime
import numpy as np
import xarray as xr

# Global attributes
CONVENTIONS = "CF-1.9"
REFERENCES = "https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9"


def dataset(
    title="Ozone data mockup",
    institution="o3skim code",
    comment="Ozone mockup data generated for testing purposes",
    start_date=datetime.datetime(2020, 1, 1),
    end_date=datetime.datetime(2020, 1, 20),
    shape=dict(latitude=50, longitude=50),
):
    shape["time"] = (end_date - start_date).days + 1
    return xr.Dataset(
        data_vars={
            "toz": toz_variable(shape=shape),
        },
        coords={
            "time": time_coordinate(start=start_date, end=end_date),
            "latitude": lat_coordinate(num=shape["latitude"]),
            "longitude": lon_coordinate(num=shape["longitude"]),
        },
        attrs={
            "Conventions": CONVENTIONS,
            "title": title,
            "institution": institution,
            "source": "Random generation",
            "references": REFERENCES,
            "history": f"{datetime.datetime.now()} - Data generated",
            "comment": comment,
        },
    )


def toz_variable(
    long_name="Total Ozone Column by Zonal Mean",
    units="mol m-2",  # Alternatives: ["DU"]
    cell_methods="time: mean (interval: 30 days) longitude: mean",
    shape=dict(time=20, latitude=50, longitude=50),
):
    return xr.Variable(
        shape.keys(),
        np.random.rand(*shape.values()),
        attrs={
            "standard_name": "atmosphere_mole_content_of_ozone",
            "long_name": long_name,
            "units": units,
            "cell_methods": cell_methods,
        },
    )


def time_coordinate(
    long_name="time",
    start=datetime.datetime(2020, 1, 1),
    end=datetime.datetime(2020, 1, 20),
):
    return xr.Variable(
        ("time",),
        xr.cftime_range(start.isoformat(), end.isoformat()),
        attrs={
            "standard_name": "time",
            "long_name": long_name,
            "axis": "T",
        },
    )


def lat_coordinate(
    long_name="latitude",
    start=90.0,
    stop=-90.0,
    num=50,
):
    return xr.Variable(
        ("latitude",),
        np.linspace(start, stop, num),
        attrs={
            "standard_name": "latitude",
            "long_name": long_name,
            "units": "degrees_north",
            "axis": "Y",
        },
    )


def lon_coordinate(
    long_name="longitude",
    start=180.0,
    stop=-180.0,
    num=50,
):
    return xr.Variable(
        ("longitude",),
        np.linspace(start, stop, num),
        attrs={
            "standard_name": "longitude",
            "long_name": long_name,
            "units": "degrees_east",
            "axis": "X",
        },
    )
