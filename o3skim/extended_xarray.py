"""
Xarray extension module to provide model class and functions to
handle tco3 and vmro3 operations and data skimming. 
"""
import logging
import xarray as xr

logger = logging.getLogger('extended_xr')


@xr.register_dataset_accessor("o3")
class O3Accessor:
    """General accessor to access all possible ozone type accessor
    using subscriptable syntax. For example:

    - `dataset.o3['tco3_zm']`  == `dataset.tco3`
    - `dataset.o3['vmro3_zm']` == `dataset.vmro3`
    """

    def __init__(self, xarray_obj):
        self._model = xarray_obj

    def __getitem__(self, o3variable):
        if o3variable == 'tco3_zm':
            return self._model.tco3
        if o3variable == 'vmro3_zm':
            return self._model.vmro3


class O3Variable:
    def __init__(self, xarray_obj, name):
        self._model = xarray_obj
        self._name = name

    @property
    def dataset(self):
        """Returns variable as Dataset and conserving attributes."""
        dataset = self._model[self._name].to_dataset()
        dataset.attrs = self._model.attrs
        return dataset


@xr.register_dataset_accessor("tco3")
class TCO3Accessor(O3Variable):
    """Total Column of Ozone accessor.
    (dataset.tco3 -acts_over-> tco3_zm variable).
    """

    def __init__(self, xarray_obj):
        O3Variable.__init__(self, xarray_obj, name='tco3_zm')


@xr.register_dataset_accessor("vmro3")
class VMRO3Accessor(O3Variable):
    """Volume Mixing Ratio of Ozone accessor.
    (dataset.vmro3 -acts_over-> vmro3_zm variable).
    """

    def __init__(self, xarray_obj):
        O3Variable.__init__(self, xarray_obj, name='vmro3_zm')
