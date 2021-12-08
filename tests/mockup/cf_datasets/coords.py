import cftime
import numpy as np
import xarray as xr


def time_coordinate(
    long_name="time",
    data=xr.cftime_range("2020-01-01", freq="MS", periods=25),
    bounds="time_bnds",
):
    return xr.DataArray(
        dims=("time",),
        data=data,
        attrs={
            "standard_name": "time",
            "long_name": long_name,
            "axis": "T",
            "bounds": bounds,
        },
    )


def lat_coordinate(
    long_name="latitude",
    data=np.linspace(-85, +85, num=18),
    bounds="lat_bnds",
):
    return xr.DataArray(
        dims=("lat",),
        data=data,
        attrs={
            "standard_name": "latitude",
            "long_name": long_name,
            "units": "degrees_north",
            "axis": "Y",
            "bounds": bounds,
        },
    )


def lon_coordinate(
    long_name="longitude",
    data=np.linspace(5.0, 355.0, num=36),
    bounds="lon_bnds",
):
    return xr.DataArray(
        dims=("lon",),
        data=data,
        attrs={
            "standard_name": "longitude",
            "long_name": long_name,
            "units": "degrees_east",
            "axis": "X",
            "bounds": bounds,
        },
    )


def bound_date(dates):
    """Shifts one possition the array, but reduces the dimension by 1.
    That reduction has to be planned before merging in the dataset.
    """
    assert dates.ndim == 1
    assert dates.dims[0] == "time"

    lower = dates[:-1].values
    upper = dates[1:].values
    return xr.DataArray(
        dims=("bounds", "time"),
        data=[lower, upper],
    )


def bound_dim(array):
    """Guess bounds values given a 1D coordinate variable.
    Assumes equal spacing on either side of the coordinate label.
    """
    assert array.ndim == 1
    dim = array.dims[0]

    diff = array.diff(dim) / 2
    lower = array[:-1] - diff
    upper = array[1:] + diff
    return xr.DataArray(
        dims=("bounds", dim),
        data=[
            np.append(lower.values, [upper[-2].values], axis=0),
            np.append([lower[1].values], upper.values, axis=0),
        ],
        attrs={"_FillValue": False},
    )
