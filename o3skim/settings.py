# Atmosphere mole content of ozone
""""Content" indicates a quantity per unit area. The "atmosphere content"
of a quantity refers to the vertical integral from the surface to the top
of the atmosphere. For the content between specified levels in the atmosphere,
standard names including "content_of_atmosphere_layer" are used.

The construction "atmosphere_mole_content_of_X" means the vertically
integrated number of moles of X above a unit area. The chemical formula for
ozone is O3. atmosphere_mole_content_of_ozone is usually measured in Dobson
Units which are equivalent to 446.2 micromoles m-2. N.B. Data variables
containing column content of ozone can be given the standard name of either
equivalent_thickness_at_stp_of_atmosphere_ozone_content or
atmosphere_mole_content_of_ozone.The latter name is recommended for
consistency with mole content names for chemical species other than ozone.
"""
TCO3_STANDARD_NAME = "atmosphere_mole_content_of_ozone"
TCO3_DATA_VARIABLE = "tco3"
TCO3_STANDARD_UNIT = "DU"
TCO3_UNITS_CONVERSION = {"DU": 1, "kg m**-2": 2.1415e-05}
