<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">o3skim</h3>

<div align="center">

  [![pipeline status](https://git.scc.kit.edu/synergy.o3as/o3skim/badges/master/pipeline.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/master)
  [![coverage status](https://git.scc.kit.edu/synergy.o3as/o3skim/badges/master/coverage.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/master)
  [![License](https://img.shields.io/badge/license-GPL-blue.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/master)
  [![Status](https://img.shields.io/badge/status-building-blue.svg)](https://git.scc.kit.edu/synergy.o3as/o3skim/-/commits/master) 

</div>

---

<p align="center"> Data pre-processing for ozone models 
    <br> 
</p>

# 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Installing](#Installing)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)
- [TODO](https://git.scc.kit.edu/synergy.o3as/o3skim/-/issues)

# 🧐 About <a name = "about"></a>
This project provides the tools to preprocess, standarise and reduce ozone data for later transfer and plot. 


# 🏁 Getting Started <a name = "getting_started"></a>
See [deployment](#deployment) for notes on how to deploy the project on a live system.

## Prerequisites
To run the project as container, install one of the following container technologies in your system:
- [docker](https://docs.docker.com/engine/install/)
- [udocker](https://indigo-dc.gitbook.io/udocker/installation_manual)

> Note udocker cannot be used to build containers, only to run them. 

> For local install and testing you need at least:
- [python 3.8](https://www.python.org/downloads/release/python-385/)
- [pip 20.0.2](https://pypi.org/)
- [gcc](https://gcc.gnu.org/)
- [g++]()

## ⛏️ Built using docker <a name = "built_using"></a>
Download the repository using git.
```sh
$ git clone git@git.scc.kit.edu:synergy.o3as/o3skim.git
```
To run as container, installation is not needed, however an image has to be build (if not downloaded form the official repository).
To build it using docker, run the following command:
```sh
$ docker build --tag o3skim .
...
Successfully built 69587025a70a
Successfully tagged o3skim:latest
```
If the build process succeded, you can list the image on the docker image list:
```sh
$ docker images
REPOSITORY                         TAG                 IMAGE ID            CREATED              SIZE
o3skim                             latest              69587025a70a        xx seconds ago      557MB
...
```

## 🔧 Running the tests <a name = "tests"></a>
First install in your system without docker, after download, use pip:
```sh
$ pip install -e .
```

After, tests can be run using 
[tox](https://tox.readthedocs.io/en/latest/)
to install it with pip run:
```sh
$ pip install tox
```

To start testing simply run:
```sh
$ tox
...
py37: commands succeeded
py38: commands succeeded
```

# 🚀 Deployment <a name = "deployment"></a>
If an image was build using docker, then just deploy the container passing the desired arguments.
For example:
```sh
$ docker run \
  -v ${PWD}/sources.yaml:/app/sources.yaml \
  -v ${PWD}/data:/app/data \
  -v ${PWD}/output:/app/output \
  o3skim --verbosity INFO
...
INFO:root:Configuration found at: './sources.yaml'
INFO:root:Loading data from './data' 
INFO:root:Skimming data to './output' 
```
For arguments description you can run `docker run o3skim --help`


# ✍️ Authors <a name = "authors"></a>
- [@V.Kozlov](https://git.scc.kit.edu/eo9869) - TBD
- [@T.Kerzenmacher](https://git.scc.kit.edu/px5501) - TBD
- [@B.steban](https://git.scc.kit.edu/zr5094) - TBD

# 🎉 Acknowledgements <a name = "acknowledgement"></a>
- 

