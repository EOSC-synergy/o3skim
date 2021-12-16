"""Simple test module for testing"""
import subprocess

import cf_xarray as cfxr
import numpy as np
from pytest import fixture, mark
from tests.utils import all_perm


def test_original_not_edited(netCDF_file):
    pass


def test_cf_conventions(netCDF_file):
    command = "cfchecks {}".format(netCDF_file)
    process = subprocess.run(command, shell=True)
    assert process.returncode == 0
