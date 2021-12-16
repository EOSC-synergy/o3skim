import datetime as dt

import cf
import numpy as np

from . import bounds, coords, variables

# Global attributes
CONVENTIONS = "CF-1.8"
REFERENCES = "https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9"

# Default dates
__date_start = cf.dt(2000, 1, 1)
__date_delta = cf.M()  # A month cf duration
__date_steps = 12
__dates = [__date_start + n * __date_delta for n in range(__date_steps)]
__time_bounds = [__date_delta.bounds(date) for date in __dates]

# Default latitudes
__lat_start = -90.0
__lat_stop = 90.0
__lat_steps = 18
__latitudes = np.linspace(__lat_start, __lat_stop, __lat_steps + 1)
__lat_bounds = list(zip(__latitudes[0:-1], __latitudes[1:]))

# Default longitudes
__lon_start = 0.0
__lon_stop = 360.0
__lon_steps = 36
__longitudes = np.linspace(__lon_start, __lon_stop, __lon_steps + 1)
__lon_bounds = list(zip(__longitudes[0:-1], __longitudes[1:]))


def toz_dataset(
    filename=f"toz-mockup.{CONVENTIONS}.nc",
    title="Ozone data mockup",
    institution="o3skim code",
    comment="Ozone mockup data generated for testing purposes",
    history=f"File created on {dt.datetime.today()}",
    time_bounds=cf.Data(__time_bounds, dtype="f8"),
    latitude_bounds=cf.Data(__lat_bounds, units="degrees_north", dtype="f8"),
    longitude_bounds=cf.Data(__lon_bounds, units="degrees_east", dtype="f8"),
):
    # Initialize variable and coordinates
    toz = variables.atmosphere_mole_content_of_ozone(
        domain_axisT=cf.DomainAxis(time_bounds.shape[0]),
        domain_axisY=cf.DomainAxis(latitude_bounds.shape[0]),
        domain_axisX=cf.DomainAxis(longitude_bounds.shape[0]),
    )
    # Set netCDF global attributes
    toz.nc_set_global_attribute("Conventions", CONVENTIONS)
    toz.nc_set_global_attribute("title", title)
    toz.nc_set_global_attribute("comment", comment)
    toz.nc_set_global_attribute("institution", institution)
    toz.nc_set_global_attribute("history", history)
    toz.nc_set_global_attribute("source", "Random generation")
    # Create the time dimension coordinate
    dimT = coords.time(bounds=time_bounds)
    bndsT = bounds.time(time_bounds)
    dimT.set_bounds(bndsT)
    # Create the latitude dimension coordinate
    dimY = coords.latitude(bounds=latitude_bounds)
    bndsY = bounds.latitude(latitude_bounds)
    dimY.set_bounds(bndsY)
    # Create the longitude dimension coordinate
    dimX = coords.longitude(bounds=longitude_bounds)
    bndsX = bounds.longitude(longitude_bounds)
    dimX.set_bounds(bndsX)
    # Insert the dimension coordinates
    toz.set_construct(dimT)
    toz.set_construct(dimY)
    toz.set_construct(dimX)
    # Save dataset
    cf.write(toz, filename, mode="w")

    # Dirtycode/Bugfix: CONVENTIONS 1.8 not written
    import netCDF4 as nc4

    ncfid = nc4.Dataset(filename, mode="a", format="NETCDF4")
    ncfid.Conventions = "CF-1.8"
    ncfid.close()
