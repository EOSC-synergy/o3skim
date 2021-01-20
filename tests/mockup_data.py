"""This modules creates mockup data for testing"""

import os

from o3skim import utils
from tests import mockup
from tests.mockup import coordinate


def _tco3(year, name='tco3'):
    return mockup.Dataset(
        var_coords={
            name: [
                coordinate.time(year),
                coordinate.lat(),
                coordinate.lon()
            ]
        },
        coords=[
            coordinate.time(year),
            coordinate.plev(),
            coordinate.lat(),
            coordinate.lon()
        ]
    )


def _vmro3(year, name='vmro3'):
    return mockup.Dataset(
        var_coords={
            name: [
                coordinate.time(year),
                coordinate.plev(),
                coordinate.lat(),
                coordinate.lon()
            ]
        },
        coords=[
            coordinate.time(year),
            coordinate.plev(),
            coordinate.lat(),
            coordinate.lon()
        ]
    )


def tco3(year_range, name='tco3'):
    for year in year_range:
        _tco3(year, name).to_netcdf(name + "_" + str(year) + ".nc")


def vmro3(year_range, name='vmro3'):
    for year in year_range:
        _vmro3(year, name).to_netcdf(name + "_" + str(year) + ".nc")


_datasets = {
    'tco3': _tco3,
    'vmro3': _vmro3
}


def combined(year_range, vars=['tco3', 'vmro3']):
    for year in year_range:
        dataset = mockup.Dataset({}, [])
        for var in vars:
            load = _datasets[var](year)
            dataset = dataset.merge(load)
        dataset.to_netcdf("merged_" + str(year) + ".nc")


def noise(name='noise'):
    """Some noise that blocks '*' wild card"""
    mockup.Dataset(
        var_coords={'noise': [coordinate.time(2000, 2010)]},
        coords=[coordinate.time(2000, 2010)]
    ).to_netcdf(name + ".nc")
