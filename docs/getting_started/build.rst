Build
===================

Download the repository at the **Build machine** using git.

.. code-block:: bash

    $ git clone git@git.scc.kit.edu:synergy.o3as/o3skim.git
    Cloning into 'o3skim'...
    ...


Build the container image at the **Build machine** using **docker**.

.. code-block:: bash

    $ docker build --tag o3skim .
    ...
    Successfully built 69587025a70a
    Successfully tagged o3skim:latest


If the build process succeded, you should see the image name on the container images list:

.. code-block:: bash

    $ docker images
    REPOSITORY                         TAG                 IMAGE ID            CREATED              SIZE
    o3skim                             latest              69587025a70a        xx seconds ago      557MB
    ...

