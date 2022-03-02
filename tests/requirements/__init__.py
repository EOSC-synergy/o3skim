"""Requirement definitions and groups"""
import numpy as np


class VariableRequirements:
    def test_toz_var_attrs(self, skimmed):
        assert skimmed.name() == "atmosphere_mole_content_of_ozone"
        assert str(skimmed.units) == "mol m-2"


class LatSkimRequirements:
    def test_no_latitude(self, skimmed):
        assert "latitude" not in [x.name() for x in skimmed.dim_coords]

    def test_cell_methods(self, skimmed):
        assert skimmed.cell_methods[-1].method == "mean"
        assert skimmed.cell_methods[-1].coord_names == ("latitude",)
        assert skimmed.cell_methods[-1].intervals == ()


class LonSkimRequirements:
    def test_no_longitude(self, skimmed):
        assert "longitude" not in [x.name() for x in skimmed.dim_coords]

    def test_cell_methods(self, skimmed):
        assert skimmed.cell_methods[-1].method == "mean"
        assert skimmed.cell_methods[-1].coord_names == ("longitude",)
        assert skimmed.cell_methods[-1].intervals == ()


class YearSkimRequirements:
    def test_1date_per_year(self, skimmed):
        diff_time = np.diff(skimmed.coord("time").bounds, 1)[:, 0]
        assert np.all(x >= 365 for x in diff_time)

    def test_cell_methods(self, skimmed):
        assert skimmed.cell_methods[-1].method == "mean"
        assert skimmed.cell_methods[-1].coord_names == ("time",)
        assert skimmed.cell_methods[-1].intervals == ("1 year",)
