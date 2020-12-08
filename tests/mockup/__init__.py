"""Mockup sub-package for tests"""

import xarray as xr
import numpy as np
# import o3skim.utils as utils


class Dataset(xr.Dataset):
    def __init__(self, var_coords, coords):
        super().__init__(
            data_vars={k: _coord_data(cx) for k, cx in var_coords.items()},
            coords=dict(coords)
        )


def _coord_data(coordinates):
    coord_names, shape = zip(*[(k, len(x)) for k, x in coordinates])
    return coord_names, np.ones(shape)

