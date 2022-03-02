"""Simple test module for testing"""
from pytest import fixture, mark

from . import (
    LatSkimRequirements,
    LonSkimRequirements,
    VariableRequirements,
    YearSkimRequirements,
)


@mark.parametrize("operations", [["year_mean"]], indirect=True)
class TestYearMean(VariableRequirements, YearSkimRequirements):
    pass


@mark.parametrize("operations", [["lat_mean"]], indirect=True)
class TestLatMean(VariableRequirements, LatSkimRequirements):
    pass


@mark.parametrize("operations", [["lon_mean"]], indirect=True)
class TestLonMean(VariableRequirements, LonSkimRequirements):
    pass
