"""Data mockup for ECMWF"""
import pandas as pd
import xarray as xr
import tests.mockup as mockup


def create_data(years):
    def date(t): return str(pd.to_datetime(t).date()).replace('-', '')
    fname = 'ESACCI-OZONE-L3S-TC-MERGED-DLR_1M-{}-fv0100.nc'
    for year in years:
        dataset = random_dataset(year)
        tx, dsx = zip(*dataset.groupby("time"))
        xr.save_mfdataset(
            [ds.drop('time') for ds in dsx],
            [fname.format(date(t)) for t in tx])


def random_tco3(year):
    coordinates = dict(
        time=mockup.time(num=12, start=year),
        longitude=mockup.lon(num=21),
        latitude=mockup.lat(num=11))
    description = "Test tco3 xarray"
    return mockup.random_array(coordinates, description)


def random_vmro3(year):
    coordinates = dict(
        time=mockup.time(num=12, start=year),
        pressure=mockup.plev(num=4),
        longitude=mockup.lon(num=21),
        latitude=mockup.lat(num=11))
    description = "Test vmro3 xarray"
    return mockup.random_array(coordinates, description)


def random_dataset(year):
    return mockup.dataset_from(
        atmosphere_mole_content_of_ozone=random_tco3(year))
