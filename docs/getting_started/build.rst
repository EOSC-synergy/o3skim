Build
===================

Download the code from the o3skim_ repository at the **Build machine**.

For example, using git_:

.. code-block:: bash

    $ git clone git@git.scc.kit.edu:synergy.o3as/o3skim.git
    Cloning into 'o3skim'...
    ...

.. _o3skim: https://git.scc.kit.edu/synergy.o3as/o3skim
.. _git: https://git-scm.com/


Build the container image at the **Build machine**.

For example, using docker_:

.. code-block:: bash

    $ docker build --tag o3skim .
    ...
    Successfully built 69587025a70a
    Successfully tagged o3skim:latest

.. _docker: https://docs.docker.com/engine/reference/commandline/build


If the build process succeded, then you should see the image name on the container images list:

.. code-block:: bash

    $ docker images
    REPOSITORY                         TAG                 IMAGE ID            CREATED              SIZE
    o3skim                             latest              69587025a70a        xx seconds ago      557MB
    ...


To use your new generated image on the **Runtime machine**, the easiest way is to 
push to a dockerhub repository. For example, with docker_:

.. code-block:: bash

    $ docker push <repository>/o3skim:<tag>

    The push refers to repository [docker.io/........./o3skim]
    ...
    7e84795fccac: Preparing 
    7e84795fccac: Layer already exists 
    ffaeb20d9e23: Layer already exists 
    4cdd6a90e552: Layer already exists 
    3e0762bebc71: Layer already exists 
    1e441fe06d90: Layer already exists 
    98ff2784e9f5: Layer already exists 
    2b99e2403063: Layer already exists 
    d0f104dc0a1f: Layer already exists 
    ...: digest: sha256:...................... size: 2004

If you do not have internet access from the **Build machine** or **Runtime machine**
it is also possible to use `docker save`_ to export your images.


.. _`docker save`: https://docs.docker.com/engine/reference/commandline/save/

