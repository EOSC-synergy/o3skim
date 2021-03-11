"""Data mockup for CCMI-1"""
import tests.mockup as mockup
import xarray as xr


def create_data(years):
    dsx = []
    for year in years:
        dsx.append(random_dataset(year))
    xr.concat(dsx).to_netcdf("o3data.nc")


def random_dataset(year):
    return mockup.dataset_from(
        tco3_zm=random_tco3(year),
        vmro3_zm=random_vmro3(year))


def random_tco3_dataset(year):
    return mockup.dataset_from(
        tco3_zm=random_tco3(year))


def random_vmro3_dataset(year):
    return mockup.dataset_from(
        vmro3_zm=random_vmro3(year))


def random_tco3(year):
    coordinates = dict(
        time=mockup.time(num=12, start=year),
        lon=mockup.lon(num=21),
        lat=mockup.lat(num=11))
    description = "Test tco3 xarray"
    return mockup.random_array(coordinates, description)


def random_vmro3(year):
    coordinates = dict(
        time=mockup.time(num=12, start=year),
        plev=mockup.plev(num=4),
        lon=mockup.lon(num=21),
        lat=mockup.lat(num=11))
    description = "Test vmro3 xarray"
    return mockup.random_array(coordinates, description)
