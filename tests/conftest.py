"""Pytest configuration file."""

import os

import o3skim
import pytest
import tests.mockup as mockup_data
import xarray

# configurations ----------------------------------------------------


# session fixtures --------------------------------------------------


# package fixtures --------------------------------------------------


# module fixtures ---------------------------------------------------


# class fixtures ----------------------------------------------------


# function fixtures -------------------------------------------------
@pytest.fixture()
def source(request):
    return request.param

@pytest.fixture()
def variable(request):
    return request.param