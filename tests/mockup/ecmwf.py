"""Data mockup for ECMWF"""
import tests.mockup as mockup


def create_data(years):
    for year in years:
        ds = random_dataset(year)
        ds.to_netcdf("era-int_sfc_{}.nc".format(year))


def random_dataset(year):
    return mockup.dataset_from(
        tco3=random_tco3(year),
        vmro3=random_vmro3(year))


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
