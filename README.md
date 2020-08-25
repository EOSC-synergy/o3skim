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

# About <a name = "about"></a>
This project provides the tools to preprocess, standarise and reduce ozone data for later transfer and plot. 


# Getting Started <a name = "getting_started"></a>
See [deployment](#deployment) for notes on how to deploy the project on a live system.

## Prerequisites
To run the project as container, you need the following systems and container technologies:
- __Build machine__ with [docker](https://docs.docker.com/engine/install/) 
- __Runtime machine__ with [udocker](https://indigo-dc.gitbook.io/udocker/installation_manual)

> Note udocker cannot be used to build containers, only to run them. 


## Built using docker <a name = "built_using"></a>
Download the repository at the __Build machine__ using git.
```sh
$ git clone git@git.scc.kit.edu:synergy.o3as/o3skim.git
Cloning into 'o3skim'...
...
```
Build the docker image at the __Build machine__ using docker.
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

## Running the tests <a name = "tests"></a>
To run tests, you need to install the tool in your system without docker.

As first step ensure you have the following dependencies:
- [python 3.8](https://www.python.org/downloads/release/python-385/)
- [pip 20.0.2](https://pypi.org/)
- [gcc](https://gcc.gnu.org/)
- [g++]()

After download and dependencies check, install with pip:
```sh
$ pip install -e .
```

Tests should run using 
[tox](https://tox.readthedocs.io/en/latest/).
To install it with pip use:
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

# Deployment <a name = "deployment"></a>
To deploy the the application using __udocker__ at the __Runtime machine__ you need:
 - Input path with data to skim, to be mounter on `/app/data` inside the container.
 - Output path for skimmed results, to be mounted on `/app/output` inside the container.
 - Configuration file with a data structure desctiption at the input path in [YAML](https://yaml.org/) format. This configuration file has to be mounted on `/app/sources.yaml` inside the container. See [sources_example.yaml](/sources_example.yaml) for a configuration example.

Once the requierement are needed, pull the image from the image registry.
For example, to pull it from the synergy-imk official registry use:
```sh
$ udocker pull synergyimk/o3skim
...
Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
...
```

Once the repository is added and the image downloaded, create the local container: 
```sh
$ udocker create --name=o3skim synergyimk/o3skim
fa42a912-b0d4-3bfb-987f-1c243863802d
```

Finally, run the container. Note the described _data_, _output_ and _sources.yaml_ have to be provided. Also it is needed to specify the user _application_ should run inside the container:
```sh
$ udocker run \
  --user=application \
  --volume=${PWD}/sources.yaml:/app/sources.yaml \
  --volume=${PWD}/data:/app/data \
  --volume=${PWD}/output:/app/output \
  o3skim --verbosity INFO
...
executing: main
...
2020-08-25 12:42:34,151 - INFO     - Configuration found at: './sources.yaml'
2020-08-25 12:42:34,152 - INFO     - Loading data from './data' 
2020-08-25 12:42:34,261 - INFO     - Skimming data to './output' 
```

For the main function description and commands help you can call:
```sh  
$ udocker run --user=application o3skim --help
...
```


# Authors <a name = "authors"></a>
- [@V.Kozlov](https://git.scc.kit.edu/eo9869) - TBD
- [@T.Kerzenmacher](https://git.scc.kit.edu/px5501) - TBD
- [@B.steban](https://git.scc.kit.edu/zr5094) - TBD

# Acknowledgements <a name = "acknowledgement"></a>
- 

