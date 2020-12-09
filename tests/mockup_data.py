"""This modules creates mockup data for testing"""

import os

from o3skim import utils
from tests import mockup
from tests.mockup import coordinate

model1_dir = "./variable_per_file"
os.makedirs(model1_dir, exist_ok=True)
with utils.cd(model1_dir):

    path = "toz"
    os.makedirs(path, exist_ok=True)
    with utils.cd(path):
        for year in range(2000, 2002):
            mockup.Dataset(
                var_coords={
                    'toz': [
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
            ).to_netcdf("toz_" + str(year) + ".nc")

    path = "vmro3"
    os.makedirs(path, exist_ok=True)
    with utils.cd(path):
        for year in range(2000, 2002):
            mockup.Dataset(
                var_coords={
                    'vmro3': [
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
            ).to_netcdf("vmro3_" + str(year) + ".nc")


model2_dir = "./variables_merged"
os.makedirs(model2_dir, exist_ok=True)
with utils.cd(model2_dir):

    for year in range(2000, 2002):
        mockup.Dataset(
            var_coords={
                'toz': [
                    coordinate.time(year),
                    coordinate.lat(),
                    coordinate.lon()
                ],
                'vmro3': [
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
        ).to_netcdf("all_" + str(year) + ".nc")

