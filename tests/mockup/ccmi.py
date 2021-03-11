"""Data mockup for CCMI-1"""
import tests.mockup as mockup


def create_data(variable, years):
    if variable == 'tco3_zm':
        for year in years:
            ds = random_toz_dataset(year)
            ds.to_netcdf("toz_bla_{}.nc".format(year))
    if variable == 'vmro3_zm':
        for year in years:
            ds = random_vmro3_dataset(year)
            ds.to_netcdf("vmro3_bla_{}.nc".format(year))


def random_toz_dataset(year):
    return mockup.dataset_from(
        toz=random_tco3(year))


def random_vmro3_dataset(year):
    return mockup.dataset_from(
        vmro3=random_vmro3(year))


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
