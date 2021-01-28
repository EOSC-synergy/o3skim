import unittest

import pandas as pd
import numpy as np
import xarray as xr
from o3skim import source


model = xr.Dataset(
    data_vars=dict(
        tco3_zm=(["lon", "lat", "time"], np.random.rand(3, 3, 25)),
        vmro3_zm=(["lon", "lat", "plev", "time"], np.random.rand(3, 3, 4, 25))
    ),
    coords=dict(
        lon=[-180, 0, 180],
        lat=[-90, 0, 90],
        plev=[1, 10, 100, 1000],
        time=pd.date_range("2000-01-01", periods=25, freq='A')
    ),
    attrs=dict(description="Test dataset")
)


class TestsModel(unittest.TestCase):

    def assertHasAttr(self, obj, intendedAttr):
        testBool = hasattr(obj, intendedAttr)
        msg = 'obj lacking an attribute. obj: %s, intendedAttr: %s' % (
            obj, intendedAttr)
        self.assertTrue(testBool, msg=msg)

    def test_dataset_has_model_accessor(self):
        self.assertHasAttr(model, 'model')
