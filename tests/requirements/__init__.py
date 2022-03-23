"""Requirement definitions and groups"""


class VariableRequirements:
    def test_standard_name(self, standard_name):
        assert standard_name == "atmosphere_mole_content_of_ozone"

    def test_standard_unit(self, units):
        assert units == "mol m-2"


class LatSkimRequirements:
    def test_no_latitude(self, skimmed):
        assert "latitude" not in [x for x in skimmed.cf.coordinates]

    def test_cell_methods(self, cell_methods):
        assert " latitude: mean" in cell_methods


class LonSkimRequirements:
    def test_no_longitude(self, skimmed):
        assert "longitude" not in [x for x in skimmed.cf.coordinates]

    def test_cell_methods(self, cell_methods):
        assert " longitude: mean" in cell_methods
