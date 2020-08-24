"""This module creates the sources objects"""
import glob
import yaml
import netCDF4
import xarray as xr
import os.path


def load(yaml_file):
    """Loads the .yaml file with the sources configurations"""
    with open(yaml_file, "r") as ymlfile:
        return yaml.load(ymlfile)


class Source:
    """Standarized datasets and methods from a data source"""

    def __init__(self, sname, collections):
        self._name = sname
        self._models = {}
        for name, variables in collections.items():
            self._models[name] = Model(variables)

    def skim(self):
        for name, model in self._models.items():
            path = self._name + "_" + name
            os.makedirs(path, exist_ok=True)
            model.skim(path)


class Model:
    """Standarised model with standarised variables"""

    def __init__(self, variables):
        self.get_tco3_zm(**variables)
        self.get_vrm_zm(**variables)

    def skim(self, path):
        if hasattr(self, '_tco3_zm'): 
            to_netcdf(path, "tco3_zm", self._tco3_zm)
        if hasattr(self, '_vrm_zm'): 
            to_netcdf(path, "vrm_zm", self._vrm_zm)

    def get_tco3_zm(self, tco3_zm=None, **kwarg):
        """Gets and standarises the tco3_zm data"""
        if tco3_zm:
            fnames = glob.glob(tco3_zm['dir'] + "/*.nc")
            with xr.open_mfdataset(fnames) as ds:
                self._tco3_zm = ds.rename({
                    tco3_zm['name']: 'tco3_zm',
                    tco3_zm['coordinades']['time']: 'time',
                    tco3_zm['coordinades']['lat']: 'lat',
                    tco3_zm['coordinades']['lon']: 'lon'
                })['tco3_zm'].to_dataset()

    def get_vrm_zm(self, vrm_zm=None, **kwarg):
        """Gets and standarises the vrm_zm data"""
        if vrm_zm:
            fnames = glob.glob(vrm_zm['dir'] + "/*.nc")
            with xr.open_mfdataset(fnames) as ds:
                self._vrm_zm = ds.rename({
                    vrm_zm['name']: 'tco3_zm',
                    vrm_zm['coordinades']['time']: 'time',
                    vrm_zm['coordinades']['lat']: 'lat',
                    vrm_zm['coordinades']['lon']: 'lon'
                })['tco3_zm'].to_dataset()


def create_empty_netCDF(fname):
    """Creates a new empty netCDF file"""
    root_grp = netCDF4.Dataset(fname, 'w', format='NETCDF4')
    root_grp.description = 'Example simulation data'
    root_grp.close()


def to_netcdf(path, name, dataset):
    """Creates or appends data to named netcdf files"""
    years, dsx = zip(*dataset.groupby("time.year"))
    fnames = [path + "/" + name + "_%s.nc" % y for y in years]
    [create_empty_netCDF(fn) for fn in fnames if not os.path.isfile(fn)]
    xr.save_mfdataset(dsx, fnames, mode='a')
