Command Line Interface
=======================

Finally, run the container. Note the described `data`, `output` and 
`sources.yaml` have to be provided. Also it is needed to specify the 
user `application` should run inside the container:

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
    ...


