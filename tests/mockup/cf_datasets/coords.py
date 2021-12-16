import cf
import numpy as np


def time(bounds):
    dimT = cf.DimensionCoordinate()
    dimT.set_property("standard_name", "time")
    dimT.nc_set_variable("time")
    data = bounds[:, 0] + np.diff(bounds) / 2
    dimT.set_data(data.squeeze())
    return dimT


def latitude(bounds):
    dimY = cf.DimensionCoordinate()
    dimY.set_property("standard_name", "latitude")
    dimY.nc_set_variable("lat")
    data = bounds[:, 0] + np.diff(bounds) / 2
    dimY.set_data(data.squeeze())
    return dimY


def longitude(bounds):
    dimX = cf.DimensionCoordinate()
    dimX.set_property("standard_name", "longitude")
    dimX.nc_set_variable("lon")
    data = bounds[:, 0] + np.diff(bounds) / 2
    dimX.set_data(data.squeeze())
    return dimX
