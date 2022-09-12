First steps
==================================

Prerequisites
----------------------------------

This software is shipped as **python3** package, therefore you need to have python3
and pip installed. If not, please check `pip documentation`_ to find out how to
install and run **pip** in your system with at least the following versions:

    =============  ===============
     software       version
    =============  ===============
     python         >= 3.8.13
     pip            >= 21.2.4
    =============  ===============

.. note:: Non admin rights? Check how to run conda_ in your machine.

.. _`pip documentation`: https://indigo-dc.gitbook.io/udocke
.. _conda: https://docs.conda.io/en/latest


Installation from source
----------------------------------

Once **python3** and **pip** are running in your system, download the package and
install it using pip:

.. code-block:: bash

    $ git clone https://git.scc.kit.edu/synergy.o3as/o3skim.git
    Cloning into 'o3skim'...
    ...
    $ cd o3skim 
    $ pip install .
    ...
    Successfully installed o3skim-...

.. note:: Some models might need the installation of xarray's IO backends, 
    (i.e. ['netcdf4', 'h5netcdf']) see:  

    https://docs.xarray.dev/en/stable/user-guide/io.html 
    https://docs.xarray.dev/en/stable/getting-started-guide/installing.html

