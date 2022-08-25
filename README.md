<p align="center">
   <img src="https://o3as.data.kit.edu/img/header-bg.jpg" width="850" height="200">
</p>

<h3 align="center">o3skim</h3>

<div align="center">

  [![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Fo3skim%2Fmain)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/o3skim/job/main)
  [![Documentation Status](https://readthedocs.org/projects/o3as/badge/?version=latest)](https://o3as.readthedocs.io/en/latest/?badge=latest)
  [![pipeline status](https://git.scc.kit.edu/synergy.o3as/o3skim/badges/main/pipeline.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/main)
  [![coverage status](https://git.scc.kit.edu/synergy.o3as/o3skim/badges/main/coverage.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/main)
  [![License](https://img.shields.io/badge/license-GPL-blue.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/main)
  [![Status](https://img.shields.io/badge/status-building-blue.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/main) 

</div>

---

<p align="center"> Data pre-processing for ozone models 
    <br> 
</p>

# 📝 Table of Contents
- [About](#about)
- [Documentation](https://o3as.readthedocs.io/en/latest)
- [Authors](#authors)
- [Issues & ToDo](https://git.scc.kit.edu/synergy.o3as/o3skim/-/issues)

# About <a name = "about"></a>
This project provides the tools to preprocess, standardize and reduce ozone data for later transfer and plot. 

## Prerequisites
This software is shipped as python3 package, therefore you need to have python3 
and pip installed. If not, please check [pip documentation](https://pip.pypa.io/en/stable/installing/) to find out how to run it in your system.

> Non admin rights? Check how to run [conda](https://docs.conda.io/en/latest/) in your machine.


# Extending functions
Create a new python module into `loadfunctions_tco3` with the name to use for model matching and a `load_tco3(model_path)` function with the load procedure. Note the `model_path` argument is a string expression which might contain more than one file. See parameter `paths` at [xarray.open_mfdataset](https://docs.xarray.dev/en/stable/generated/xarray.open_mfdataset.html).

Some examples:
 - `CCMI-1_ACCESS` matches `CCMI-1_ACCESS_CCM-refC2` and `CCMI-1_ACCESS_ACCESS-CCM`
 - `CCMI-1_IPSL` matches `CCMI-1_IPSL-refC2` and `CCMI-1_IPSL_IPSL-senC2fGHG`
 - `ECMWF_C3S` matches `ECMWF_C3S` and `ECMWF_C3S_ERA5`

Functions sum-up:
 - For tco3 load functions, subpackage=`loadfunctions_tco3`, function=`load_tco3(model_path) -> dataset`
 - For zmo3 load functions, subpackage=`loadfunctions_zmo3`, function=`load_zmo3(model_path) -> dataset`


# Testing <a name = "testing"></a>
Testing is based on [sqa-baseline](https://indigo-dc.github.io/sqa-baseline/) criteria. On top, [tox](https://tox.readthedocs.io/en/latest/) automation is used to simplify the testing process.

To run unit and functional tests with coverage use:
```sh
$ tox
```

If you want to test new load modules, create a folder into the corresponding `./tests/dataset_*` directory with the name of the model to use on the load function. Before adding test data into the folder consider the following:
 - Ensure your test sample does not contain any private information, for example emails.
 - Minimize the sample data as much as possible. Files size impact repository size and testing speed. 

# Documentation <a name = "doc"></a>
All o3as project module documents can be found at [o3as.readthedocs.io](https://o3as.readthedocs.io/en/latest/). 


# Authors <a name = "authors"></a>
- [@V.Kozlov](https://git.scc.kit.edu/eo9869)
- [@T.Kerzenmacher](https://git.scc.kit.edu/px5501)
- [@B.Esteban](https://git.scc.kit.edu/zr5094)

