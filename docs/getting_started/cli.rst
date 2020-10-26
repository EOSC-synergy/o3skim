Command Line Interface
=======================

Usage:

.. code-block:: bash

    usage: main [-h] [-f SOURCES_FILE] [-s {year,decade}]
                [-v {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

To run the the application using **udocker** at the **Runtime machine** 
you need to provide the following volumes to the container:

 - --volume, mount `/app/data`: Input path with data to skim.
 - --volume, mount `/app/output`: Output path for skimmed results.
 - --volume, mount `/app/sources.yaml`: Configuration file with a data structure 
   description at the input path in YAML_ format.
   See :doc:`/user_guide/source-file` for a configuration example.

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
      o3skim --verbosity INFO
    ...
    executing: main
    ...
    2020-08-25 12:42:34,151 - INFO     - Configuration found at: './sources.yaml'
    2020-08-25 12:42:34,152 - INFO     - Loading data from './data' 
    2020-08-25 12:42:34,261 - INFO     - Skimming data to './output' 


For the main function description and commands help you can call:

.. code-block:: bash

    $ udocker run --user=application o3skim --help


As optional arguments, it is possible to indicate:

 - -h, --help: show this help message and exit
 - -f, --sources_file SOURCES_FILE: Custom sources YAML configuration. (default: ./sources.yaml)
 - -s, --split_by {year,decade}: Period time to split output (default: None)
 - -v, --verbosity {DEBUG,INFO,WARNING,ERROR,CRITICAL}: Sets the logging level (default: ERROR)

Note that SOURCES_FILE is only modified for development purposes as usually any 
file from host can be mounted using the container directive '--volume'. 

