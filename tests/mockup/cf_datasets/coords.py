import cf
import numpy as np
import xarray as xr

__coord_T = xr.cftime_range("2020-01-01", freq="MS", periods=25)
__coord_Y = np.linspace(-85, +85, num=18)
__coord_X = np.linspace(5.0, 355.0, num=36)


def time(
    data=cf.dt_vector(__coord_T, calendar="standard"),
    units="days since 2020-01-01",
):
    dimT = cf.DimensionCoordinate()
    dimT.set_property("standard_name", "time")
    dimT.set_property("units", units)
    dimT.set_data(cf.Data(data, dtype="f8"))
    return dimT


def latitude(
    data=__coord_Y,
    units="degrees_north",
):
    dimY = cf.DimensionCoordinate()
    dimY.set_property("standard_name", "latitude")
    dimY.set_property("units", units)
    dimY.set_data(cf.Data(data, dtype="f8"))
    return dimY


def longitude(
    data=__coord_X,
    units="degrees_east",
):
    dimX = cf.DimensionCoordinate()
    dimX.set_property("standard_name", "longitude")
    dimX.set_property("units", units)
    dimX.set_data(cf.Data(data, dtype="f8"))
    return dimX
