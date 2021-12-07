import cftime
import numpy as np
import xarray as xr


def time_coordinate(
    long_name="time",
    data=xr.cftime_range("2020-01-01T12:00:00", periods=20),
):
    return xr.DataArray(
        dims=("time",),
        data=data,
        attrs={
            "standard_name": "time",
            "long_name": long_name,
            "axis": "T",
        },
    )


def time_bounds(dates):
    """Guess bounds values given a 1D coordinate variable.
    Assumes equal spacing on either side of the coordinate label.
    """
    assert dates.ndim == 1
    unit = "microsec since 1970-01-01 00:00:00"
    calendar = dates.values[0].calendar
    array = xr.DataArray(cftime.date2num(dates, unit))

    dim = array.dims[0]
    diff = array.diff(dim) / 2
    lower = array[:-1] - diff
    upper = array[1:] + diff
    lower = xr.concat([lower, upper[-2]], dim=dim)
    upper = xr.concat([lower[1], upper], dim=dim)

    return xr.concat(
        [
            xr.DataArray(cftime.num2date(lower, unit, calendar=calendar)),
            xr.DataArray(cftime.num2date(upper, unit, calendar=calendar)),
        ],
        dim="bounds",
    )


def lat_coordinate(
    long_name="latitude",
    data=np.linspace(-85, +85, num=18),
):
    return xr.DataArray(
        dims=("lat",),
        data=data,
        attrs={
            "standard_name": "latitude",
            "long_name": long_name,
            "units": "degrees_north",
            "axis": "Y",
        },
    )


def lon_coordinate(
    long_name="longitude",
    data=np.linspace(5.0, 355.0, num=36),
):
    return xr.DataArray(
        dims=("lon",),
        data=data,
        attrs={
            "standard_name": "longitude",
            "long_name": long_name,
            "units": "degrees_east",
            "axis": "X",
        },
    )


def dim_bounds(array):
    """Guess bounds values given a 1D coordinate variable.
    Assumes equal spacing on either side of the coordinate label.
    """
    assert array.ndim == 1

    dim = array.dims[0]
    diff = array.diff(dim) / 2
    lower = array[:-1] - diff
    upper = array[1:] + diff
    lower = xr.concat([lower, upper[-2]], dim=dim)
    upper = xr.concat([lower[1], upper], dim=dim)

    return xr.concat([lower, upper], dim="bounds")
