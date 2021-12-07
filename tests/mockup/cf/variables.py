import xarray as xr
import numpy as np


def toz_variable(
    long_name="Total Ozone Column",
    units="mol m-2",  # Alternatives: ["DU"]
    cell_methods="time: mean (interval: 1 days) longitude: mean",
    shape=dict(time=20, lat=18, lon=36),
):
    return xr.Variable(
        dims=shape.keys(),
        data=np.random.rand(*shape.values()),
        attrs={
            "standard_name": "atmosphere_mole_content_of_ozone",
            "long_name": long_name,
            "units": units,
            "cell_methods": cell_methods,
        },
    )
