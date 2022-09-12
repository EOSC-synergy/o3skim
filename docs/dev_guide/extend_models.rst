Extending o3skim models
=======================
To simplify extension of the library by scientist, this library has adopted
a "plugin" philosophy. Inside the library, you can find a set of subpackages
(folders in the folder o3skim) with multiple modules, each with the name of
the model it provides support for:

 - **o3skim/loadfunctions_tco3**: Modules to load TCO3 models.
 - **o3skim/loadfunctions_zmo3**: Modules to load ZMO3 models.

This allows extending o3skim load functions argument *model* with your own
function scripts. For example, the function call
:code:`o3skim.load_tco3(model_path, model='CCMI-1_MODEL1')` will make use
of *CCMI-1_MODEL1.py* module located at *loadfunctions_tco3*.


First, add representative datasets for testing your load modules
----------------------------------------------------------------
When skimming ozone data, the most difficult challenge is to produce
normalized datasets from multiple sources. To do so, testing is the most
fundamental pillar to ensure all loaded datasets share the same structure
and features.

Tests are always executed when calling `pytest`, `tox` or any `CICD` means.
In order to ensure your modules follow the normalization requirements,
you should add a small but still representative dataset for the model load
function you are about to create into the required folder:

 - **tests/datasets_tco3**: Datasets to test TCO3 load functions.
 - **tests/datasets_zmo3**: Datasets to test ZMO3 load functions.

You can see examples of representative datasets for the already supported
load functions inside the same folders. 

.. note::
    Dimensions of size 1 might not be enough representative for the data
    depending on your load function. For example, imagine a case where you
    apply monthly average on daily data, 1 size on time dimension might pass
    testing but fail in real usage.

The testing dataset data should be placed inside a folder with the name of
model argument to be tested. Here is an example of how the directory should
look:

.. code-block:: bash

    $ tree tests/datasets_tco3
    tests/datasets_tco3
    ├── CCMI-1_ACCESS_ACCESS-CCM-refC2
    │   └── toz_monthly_ACCESS-CCM_refC2_r1i1p1_196001-196104.nc
    ├── CCMI-1_CCCma_CMAM-refC2
    │   ├── toz_monthly_CMAM_refC2_r1i1p1_196001-196008.nc
    │   └── toz_monthly_CMAM_refC2_r1i1p1_196009-196104.nc
    └── SBUV_GSFC_merged-SAT-ozone
        └── sbuv.v86.mod_v10.70-18.za.txt

Once you have added your dataset example for testing, next time the software
tests are running, a new parameter with the name of your file 
(i.e. *[CCMI-1_ACCESS_ACCESS-CCM-refC2]*) will be added to the following list of
test functions:

 - test_attributes: Checks the required CF Convention attributes.
 - test_coord_lat: Checks the correct latitude coordinates attributes.
 - test_coord_lon: Checks the correct longitude coordinates attributes.
 - test_coord_plev: Checks the correct air pressure coordinates attributes.
 - test_coord_time: Checks the correct time coordinates attributes.
 - test_operations: Checks compatibility with Xarray operations (i.e. mean).
 - test_variable: Checks the correct ozone variable attributes.

.. image:: ../_static/check_list.png
   :width: 600

This way it is ensure that your load function will return a correct 
*xarray CF object*.

.. note::
    When adding test datasets, take into consideration the following:

     - Test samples are stored in a public repository, therefore should not contain private information, check attributes.
     - Time for testing and repository size are proportional to the test samples. Minimize datasets as much as possible but still representative.


Once the dataset is added, you can follow the details described at
:doc:`testing` to install the required tools for testing and run 
the desired tox command at :doc:`commands` to start the validation process.
If you have not created yet the correct load module you will see that tests
fail when dataset folder is passed as *model* argument. 


Second, add your module and model load function 
-----------------------------------------------

Load functions for load_tco3
"""""""""""""""""""""""""""""""
You can add new modules to the subpackage **o3skim/loadfunctions_tco3**
in order to extend models available for the function `o3skim.load_tco3`.
This function should accept the paths expression to the dataset netCDF files
and return the final standardized Dataset.

.. code-block:: python

    def load_tco3(model_path):
        """Loads and returns a model and the dataset attributes.
        :param model_path: Paths expression to the dataset netCDF files
        :return: Standardized Dataset
        """
        ...
        return dataset

This function will be tested with the testing datasets models
from **tests/datasets_tco3** matching the folder name start
(i.e. `CCMI-1_GSFC` for `CCMI-1_GSFC_X-refC1` and `CCMI-1_GSFC_X-refC2`).


Load functions for load_zmo3
"""""""""""""""""""""""""""""""
You can add new modules to the subpackage **o3skim/loadfunctions_zmo3**
in order to extend models available for the function `o3skim.load_zmo3`.
This function should accept the paths expression to the dataset netCDF files
and return the final standardized Dataset.

.. code-block:: python

    def load_zmo3(model_path):
        """Loads and returns a model and the dataset attributes.
        :param model_path: Paths expression to the dataset netCDF files
        :return: Standardized Dataset
        """
        ...
        return dataset

This function will be tested with the testing datasets models
from **tests/datasets_zmo3** matching the folder name start
(i.e. `CCMI-1_GSFC` for `CCMI-1_GSFC_X-refC1` and `CCMI-1_GSFC_X-refC2`).


.. note::
    Feel free to use any of the already existing modules as examples for
    the extension process if you do not know how to start.
