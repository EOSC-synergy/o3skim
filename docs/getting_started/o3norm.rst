o3norm
=======================

You can standardize a dataset from any sources using the provided command
**o3norm** when installing the package.

.. code-block:: bash

  usage: o3norm [-h] [-v {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-t TARGET]
                (--tco3_zm | --vmro3_zm)
                {CCMI-1,ECMWF,ESACCI,SBUV} ... 


This command loads the model from the specified sources and produces an 
standardized netCDF_ output with the following structure:

.. code-block:: 

  Dimensions:   (lat: _, lon: _, plev: _, time: _)
  Coordinates:
    * time      (time) datetime64[ns] ____-__-__ ... ____-__-__T__:__:__
    * plev      (plev) float64 ___._ ... ___._
    * lon       (lon) float64 ___._ ... ___._
    * lat       (lat) float64 ___._ ... ___._
  Data variables:
      tco3_zm   (time, lon, lat) float64 __
      vmro3_zm  (time, plev, lon, lat) float64 __
      ...
  Attributes:
      <The original dataset attributes> 

.. _netCDF: https://www.unidata.ucar.edu/software/netcdf


This can help you to work easier with multiple sources having a common data
structure for your data.

The usage is very simple, call the **o3norm** command followed by the specific
model type you would like to load as a *Sub-command*. Note that there are 
general optional arguments common to all source types (for example --target) 
and specific to each source type (for example --delimiter in the case of SBUV).

.. code-block:: 

  positional arguments (Sub-commands):
    {CCMI-1,ECMWF,ESACCI,SBUV}
                          Sub-commands
      CCMI-1              CCMI-1 Source input
      ECMWF               ECMWF Source input
      ESACCI              ESACCI Source input
      SBUV                SBUV Source input

  optional arguments:
    -h, --help            show this help message and exit
    -v {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --verbosity {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                          Sets the logging level (default: INFO)
    -t TARGET, --target TARGET
                          Target netCDF file (default: o3data)
    --tco3_zm             Standardization for total column ozone
    --vmro3_zm            Standardization for volume mixing ratio ozone


You can use the *optional argument* **--help** to see the *Command* and 
*Sub-command* instructions. For example, to see the options available for the
*CCMI-1* you can use:

.. code-block::

  $ o3norm CCMI-1 --help
  usage: o3norm CCMI-1 [-h] [--time TIME] [--plev PLEV] [--lat LAT] [--lon LON]
                      variable paths [paths ...]
  ...


As last example, the following commands shows how to produce an output of 
standardized netCDF_ files at the file *mydata.nc* using the files provided
from a CCMI-1 source:

.. code-block::

  $ o3norm --tco3_zm -t mydata.nc CCMI-1 toz Ccmi/some_path/*.nc
  $ o3norm --vmro3_zm -t mydata.nc CCMI-1 vmro3 Ccmi/some_path/*.nc
  ...

See the first command loads the **toz** from the source as **tco3_zm** and the
second the **vmro3** as **vmro3_zm**. Both commands are targeting the file
*mydata.nc*, therefore that file will contain the information about the 2 
variables.

.. _netCDF: https://www.unidata.ucar.edu/software/netcdf
