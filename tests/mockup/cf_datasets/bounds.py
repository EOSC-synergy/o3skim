import cf


def time(dimT, data):
    bnds = cf.Bounds()
    bnds.nc_set_variable("time_bnds")
    bnds.set_data(cf.Data(data, dtype="f8"))
    dimT.set_bounds(bnds)
    return bnds


def latitude(dimY, data):
    bnds = cf.Bounds()
    bnds.nc_set_variable("lat_bnds")
    bnds.set_data(cf.Data(data, dtype="f8"))
    dimY.set_bounds(bnds)
    return bnds


def longitude(dimX, data):
    bnds = cf.Bounds()
    bnds.nc_set_variable("lon_bnds")
    bnds.set_data(cf.Data(data, dtype="f8"))
    dimX.set_bounds(bnds)
    return bnds
