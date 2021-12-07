import datetime

import xarray as xr

from . import coords, variables


# Global attributes
CONVENTIONS = "CF-1.9"
REFERENCES = "https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9"
DAY = datetime.timedelta(days=1)


def toz_dataset(
    title="Ozone data mockup",
    institution="o3skim code",
    comment="Ozone mockup data generated for testing purposes",
    history=f"{datetime.datetime.now()} - Data generated",
    toz=variables.toz_variable(),
    time=coords.time_coordinate(),
    latitude=coords.lat_coordinate(),
    longitude=coords.lon_coordinate(),
):
    return xr.Dataset(
        data_vars={
            "toz": toz,
        },
        coords={
            "time": time[:-1],
            "time_bnds": coords.bound_date(time),
            "lat": latitude,
            "lat_bnds": coords.bound_dim(latitude),
            "lon": longitude,
            "lon_bnds": coords.bound_dim(longitude),
        },
        attrs={
            "Conventions": CONVENTIONS,
            "title": title,
            "institution": institution,
            "source": "Random generation",
            "references": REFERENCES,
            "history": history,
            "comment": comment,
        },
    )
