Deployment
==================================

To deploy the the application using **udocker** at the **Runtime machine** 
you need:

 - Input path with data to skim, to be mounter on `/app/data` inside the 
   container.
 - Output path for skimmed results, to be mounted on `/app/output` inside
   the container.
 - Configuration file with a data structure desctiption at the input path
   in YAML_ format. This configuration file has to be mounted on 
   `/app/sources.yaml` inside the container. 
   See [sources_example.yaml](/sources_example.yaml) for a configuration 
   example.

.. _YAML: https://yaml.org/


Once the requierement are needed, pull the image from the image registry.
For example, to pull it from the synergy-imk official registry use:

.. code-block:: bash

    $ udocker pull synergyimk/o3skim
    ...
    Downloading layer: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
    ...


Once the repository is added and the image downloaded, create the local container: 

.. code-block:: bash

    $ udocker create --name=o3skim synergyimk/o3skim
    fa42a912-b0d4-3bfb-987f-1c243863802d

