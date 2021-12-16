import cf


def time(data):
    bounds = cf.Bounds()
    bounds.nc_set_variable("time_bnds")
    bounds.set_data(data)
    return bounds


def latitude(data):
    bounds = cf.Bounds()
    bounds.nc_set_variable("lat_bnds")
    bounds.set_data(data)
    return bounds


def longitude(data):
    bounds = cf.Bounds()
    bounds.nc_set_variable("lon_bnds")
    bounds.set_data(data)
    return bounds
