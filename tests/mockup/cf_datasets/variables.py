import cf
import numpy as np


def atmosphere_mole_content_of_ozone(
    long_name="Total Ozone Column",
    units="mol m-2",  # Alternatives: ["DU"]
    domain_axisT=cf.DomainAxis(10),
    domain_axisY=cf.DomainAxis(18),
    domain_axisX=cf.DomainAxis(36),
):
    toz = cf.Field()
    # Set variable attributes
    toz.set_property("standard_name", "atmosphere_mole_content_of_ozone")
    toz.set_property("long_name", long_name)
    toz.set_property("units", units)
    # Set variable data
    shape = (domain_axisT.size, domain_axisY.size, domain_axisX.size)
    toz.set_data(cf.Data(np.ndarray(shape)))
    toz.nc_set_variable("toz")
    # Insert domain axis constructs into field.
    axisT = toz.set_construct(domain_axisT, key="domainaxis0", copy=False)
    axisY = toz.set_construct(domain_axisY, key="domainaxis1", copy=False)
    axisX = toz.set_construct(domain_axisX, key="domainaxis2", copy=False)
    toz.set_data_axes(("domainaxis0", "domainaxis1", "domainaxis2"))
    # Create the cell method constructs
    area_method = cf.CellMethod(axes="area", method="mean")
    toz.set_construct(area_method)
    time_method = cf.CellMethod(axes=axisT, method="maximum")
    toz.set_construct(time_method)
    # Return toz field
    return toz
