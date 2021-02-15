Command Line Interface
=======================

Usage:

.. code-block:: bash

    usage: main [-h] [-f SOURCES_FILE] [-s {year,decade}]
                [-v {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                {lon_mean,lat_mean} [{lon_mean,lat_mean} ...]

To run the the application using **udocker** at the **Runtime machine** 
you need to provide the following volumes to the container:

 - --volume, mount `/app/data`: Input path with data to skim.
 - --volume, mount `/app/output`: Output path for skimmed results.
 - --volume, mount `/app/sources.yaml`: Configuration file with a data structure 
   description at the input path in YAML_ format.
   See :doc:`../getting_started/source-file` for a configuration example.

.. _YAML: https://yaml.org/


Also, in the specific case of udocker_, it is needed to specify that the 
user `application` should run inside the container:

.. _udocker: https://indigo-dc.gitbook.io/udocker


For example,to run the container using udocker_ use the following:

.. code-block:: bash

    $ udocker run \
      --user=application \
      --volume=${PWD}/sources.yaml:/app/sources.yaml \
      --volume=${PWD}/data:/app/data \
      --volume=${PWD}/output:/app/output \
      o3skim --verbosity INFO lon_mean
    ...
    executing: main
    ...
    2020-08-25 12:42:34,151 - INFO     - Configuration found at: './sources.yaml'
    2020-08-25 12:42:34,152 - INFO     - Loading data from './data' 
    2020-08-25 12:42:34,261 - INFO     - Skimming data to './output' 


For the main function description and commands help you can call:

.. code-block:: bash

    $ udocker run --user=application o3skim --help


Where positional arguments are the o3skim operations to perform:

.. code-block:: bash

  o3skim is a tool for data pre-processing of ozone applications:
  - lon_mean: Mean operation over longitude axis.
  - lat_mean: Mean operation over latitude axis.

  positional arguments:
    {lon_mean,lat_mean}   o3skim operations to perform

  optional arguments:
    -h, --help            Show this help message and exit
    -f SOURCES_FILE, --sources_file SOURCES_FILE
                          Custom sources YAML configuration; default:./sources.yaml
    -s {year,decade}, --split_by {year,decade}
                          Period time to split output; default: None
    -v {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --verbosity {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                          Sets the logging level; default: ERROR

Note that SOURCES_FILE is only modified for development purposes as usually any 
file from host can be mounted using the container directive '--volume'. 

