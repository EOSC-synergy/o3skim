<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">o3skim</h3>

<div align="center">

  [![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2Fo3skim%2Ftest)](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/o3skim/job/master)
  [![Documentation Status](https://readthedocs.org/projects/o3as/badge/?version=latest)](https://o3as.readthedocs.io/en/latest/?badge=latest)
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
- [Build using docker](#build)
- [Run using udocker](#deployment)
- [Testing](#testing)
- [Documentation](https://o3as.readthedocs.io/en/latest)
- [Authors](#authors)
- [TODO](https://git.scc.kit.edu/synergy.o3as/o3skim/-/issues)

# About <a name = "about"></a>
This project provides the tools to preprocess, standardize and reduce ozone data for later transfer and plot. 

## Prerequisites
To run the project as container, you need the following systems and container technologies:
- __Build machine__ with [docker](https://docs.docker.com/engine/install/) 
- __Runtime machine__ with [udocker](https://indigo-dc.gitbook.io/udocker/installation_manual)

> Note udocker cannot be used to build containers, only to run them. 


# Built using docker <a name = "build"></a>
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
If the build process succeeded, you can list the image on the docker image list:
```sh
$ docker images
REPOSITORY                         TAG                 IMAGE ID            CREATED              SIZE
o3skim                             latest              69587025a70a        xx seconds ago      557MB
...
```

# Run using udocker <a name = "deployment"></a>
To deploy the the application using __udocker__ at the __Runtime machine__ you need:
 - Input path with data to skim, to be mounter on `/app/data` inside the container.
 - Output path for skimmed results, to be mounted on `/app/output` inside the container.
 - Configuration file with a data structure description at the input path in [YAML](https://yaml.org/) format.
   This configuration file has to be mounted on `/app/sources.yaml` inside the container.

Once the requirement are completed, pull the image from the image registry.
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

# Testing <a name = "testing"></a>
Testing is based on [sqa-baseline](https://indigo-dc.github.io/sqa-baseline/) criteria. On top, [tox](https://tox.readthedocs.io/en/latest/) automation is used to simplify the testing process.

To run unit and functional tests with coverage use:
```sh
$ tox
```


# Documentation <a name = "doc"></a>
All o3as project module documents can be found at [o3as.readthedocs.io](https://o3as.readthedocs.io/en/latest/). 


# Authors <a name = "authors"></a>
- [@V.Kozlov](https://git.scc.kit.edu/eo9869)
- [@T.Kerzenmacher](https://git.scc.kit.edu/px5501)
- [@B.Esteban](https://git.scc.kit.edu/zr5094)

