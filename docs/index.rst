************************************************
Data skimming for ozone assessment.
************************************************

**o3skim** is an open source project and Python package that provides the 
tools to pre-process, standardize and reduce ozone data from netCDF_ models to
simplify and speed up ozone data transfer and plot.

.. _netCDF: http://www.unidata.ucar.edu/software/netcdf


Getting started
=========================================

* Which :doc:`getting_started/first_steps` you need to start.
* How to use :doc:`getting_started/load_tco3` to load normalized tco3 models.
* How to use :doc:`getting_started/load_zmo3` to load normalized zmo3 models.
* How to use :doc:`getting_started/lon_mean` to reduce model longitude.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Getting started

   getting_started/first_steps
   getting_started/load_tco3
   getting_started/load_zmo3
   getting_started/lon_mean

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Examples:

   examples/multisource_tco3skim
   examples/tco3skim_ccmi-1
   examples/zmo3load_ccmi-1


Developer guide
=========================================

* Check the :doc:`dev_guide/extend_models` to extend the functionality.
* Check the :doc:`dev_guide/testing` to test the package and functions.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Developer guide:

   dev_guide/extend_models
   dev_guide/testing






Authors 
=========================================

- `@T.Kerzenmacher <https://git.scc.kit.edu/px5501>`_ - Data scientist at KIT-IMK_
- `@V.Kozlov <https://git.scc.kit.edu/eo9869>`_ - Code developer at KIT-SCC_
- `@B.Esteban <https://git.scc.kit.edu/zr5094>`_ - Code developer at KIT-SCC_

.. _KIT-IMK: https://www.imk.kit.edu/english/index.php
.. _KIT-SCC: https://www.scc.kit.edu/en/index.php


CF conventions
=========================================
When skimming ozone data, one of the main challenges is to produce normalized
datasets from multiple sources that can be used laster into the same automated
procedures.
To make this possible, the `CF conventions`_ are designed to promote the
processing and sharing of files created with the NetCDF. 

However, although conventions provide sensible recommendations and methods,
in practice not all scientist might follow them strictly. Additionally in
multiple cases, authors might add personal information or extend datasets
with variables that interferences with the correct functionality of popular
python numeric libraries (i.e. xarray_).

.. _`CF conventions`: https://cfconventions.org/
.. _xarray: https://www.imk.kit.edu/english/index.php
