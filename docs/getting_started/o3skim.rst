o3skim
=======================

You can reduce an output dataset produced by **o3norm** using the provided
command **o3skim** when installing the package.

.. code-block:: bash

  usage: o3skim [-h] [-v {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-o OUTPUT]
                [--lon_mean] [--lat_mean] [--year_mean]
                paths [paths ...]


This command loads the model from the specified paths and produces a set
of standardized netCDF_ files. The output data are splitted into one file
per variable at the original dataset. For example, skimming a dataset with
**tco3_zm** and **vmro3_zm** produces the following output at the specified
folder:

.. code-block:: bash

  $ tree output_folder
  output_folder/
  ├── tco3_zm.nc
  └── vmro3_zm.nc

.. _netCDF: https://www.unidata.ucar.edu/software/netcdf

The structure of each output file will depend on the variable it contains
(for example, tco3_zm does not contain *plev* coordinates) and the skimming
operations performed (for example, lon_mean reduces the *lon* coordinate).
This reduces the transference size by transferring only the files with the 
intended variables. 

The usage is quite simple, call the **o3skim** command followed by the
operations you would like to performed as *optional arguments* and with
the paths to the dataset you would like to reduce.

.. code-block:: bash

  positional arguments:
    paths                 Paths to netCDF files with the data to skim

  optional arguments:
    -h, --help            show this help message and exit
    -v {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --verbosity {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                          Sets the logging level (default: INFO)
    -o OUTPUT, --output OUTPUT
                          Folder for output files (default: .)

  operations:
    --lon_mean            Longitudinal mean across the dataset
    --lat_mean            Latitudinal mean across the dataset
    --year_mean           Time average across the year


As an example, the following command shows how to reduce a dataset running
an average mean over the latitude and longitude coordinates at the folder 
*skimmed_model*:

.. code-block::

  $ o3skim -o skimmed_model --lon_mean --lat_mean mydata.nc
  ...
  $ tree skimmed_model
  skimmed_model/
  └── tco3_zm.nc


From this example, we can foreseen that the original dataset *mydata.nc* 
contained only **tco3_zm** information. The expected structure for the
*tco3_zm.nc* dataset would be as follows:

.. code-block:: 

  Dimensions:   (time: _)
  Coordinates:
    * time      (time) datetime64[ns] ____-__-__ ... ____-__-__T__:__:__
  Data variables:
      tco3_zm   (time) float64 __
  Attributes:
      <The original dataset attributes> 

