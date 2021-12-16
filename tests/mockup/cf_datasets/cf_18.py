import datetime as dt

import cf

from . import bounds, coords, variables

# Global attributes
CONVENTIONS = "CF-1.8"
REFERENCES = "https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9"


def toz_dataset(
    filename=f"toz.{CONVENTIONS}.nc",
    title="Ozone data mockup",
    institution="o3skim code",
    comment="Ozone mockup data generated for testing purposes",
    history=f"File created on {dt.datetime.today()}",
    time=coords.time(),
    latitude=coords.latitude(),
    longitude=coords.longitude(),
):
    # Initialize variable and coordinates
    toz = variables.atmosphere_mole_content_of_ozone(
        domain_axisT=cf.DomainAxis(time.size),
        domain_axisY=cf.DomainAxis(latitude.size),
        domain_axisX=cf.DomainAxis(longitude.size),
    )
    # Set netCDF global attributes
    toz.nc_set_global_attribute("Conventions", CONVENTIONS)
    toz.nc_set_global_attribute("title", title)
    toz.nc_set_global_attribute("comment", comment)
    toz.nc_set_global_attribute("institution", institution)
    toz.nc_set_global_attribute("history", history)
    toz.nc_set_global_attribute("source", "Random generation")
    # Insert the dimension coordinate constructs into the fields
    toz.set_construct(time)
    toz.set_construct(latitude)
    toz.set_construct(longitude)
    # Save dataset
    cf.write(toz, filename, mode="w")

    # Dirtycode/Bugfix: CONVENTIONS 1.8 not written
    import netCDF4 as nc4

    ncfid = nc4.Dataset(filename, mode="a", format="NETCDF4")
    ncfid.Conventions = "CF-1.8"
    ncfid.close()
