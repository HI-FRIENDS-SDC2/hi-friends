Workflow installation
=====================

This sections starts with the list of the main software used by the
workflow, and a detailed list of all the dependencies required to
execute it. Please, note that it is not needed to install these
dependencies because the workflow will that automatically. The
instructions below descripbe how to install the workflow locally (just
by installing snakemake with conda, and snakemake will take care of all
the rest). There are also instructions to use the containerized version
of the workflow, using either docker, singularity or podman.

Dependencies
------------

The main software dependencies are:

-  `Sofia2 <https://github.com/SoFiA-Admin/SoFiA-2/>`__ (version 2.3.0)
   which is licensed under the `GNU General Public License
   v3.0 <https://github.com/SoFiA-Admin/SoFiA-2/blob/master/LICENSE>`__
-  `Conda <https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh>`__
   (version 4.9.2) which is released under the `3-clause BSD
   license <https://docs.conda.io/en/latest/license.html>`__
-  `Snakemake <https://snakemake.readthedocs.io/en/stable/>`__
   (snakemake-minimal version 6.5.3) which is licensed under the `MIT
   License <https://snakemake.readthedocs.io/en/stable/project_info/license.html>`__
-  `Spectral-cube <https://spectral-cube.readthedocs.io/en/latest/installing.html#installation>`__\ (version
   0.5.0) which is licensed under a `BSD 3-Clause
   license <https://github.com/radio-astro-tools/spectral-cube/blob/master/LICENSE.rst>`__
-  `Astropy <https://www.astropy.org>`__\ (version 4.2.1) which is
   licensed under a `3-clause BSD style
   license <https://docs.astropy.org/en/stable/license.html?highlight=license#astropy-license>`__

The requirements of the HI-FRIENDS data challenge solution workflow are
self-contained, and they will be retrieved and installed during
execution using ``conda``. To run the pipeline you need to have
`snakemake <https://snakemake.readthedocs.io/en/stable/>`__ installed.
This can be obtained from the ``environment.yml`` file in the repository
as explained in the next Section. The workflow uses the following
packages:

::

     - astropy=4.2.1
     - astropy=4.3.post1
     - astroquery=0.4.1
     - astroquery=0.4.3
     - dask=2021.3.1
     - gitpython=3.1.18
     - ipykernel=5.5.5
     - ipython=7.22.0
     - ipython=7.25.0
     - ipython=7.26.0
     - jinja2=3.0.1
     - jupyter=1.0.0
     - jupyterlab=3.0.16
     - jupyterlab_pygments=0.1.2
     - matplotlib=3.3.4
     - msgpack-python=1.0.2
     - networkx=2.6.1
     - numpy=1.20.1
     - numpy=1.20.3
     - pandas=1.2.2
     - pandas=1.2.5
     - pip=21.0.1
     - pygments=2.9.0
     - pygraphviz=1.7
     - pylint=2.9.6
     - pytest=6.2.4
     - python-wget=3.2
     - python=3.8.6
     - python=3.9.6
     - pyyaml=5.4.1
     - scipy=1.7.0
     - seaborn=0.11.1
     - snakemake-minimal=6.5.3
     - sofia-2=2.3.0
     - spectral-cube=0.5.0
     - wget=1.20.1

This list can also be found in `all
dependencies <https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/docs/materials/all_dependencies.txt>`__.
The links where all the software can be found is in `all
links <https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/docs/materials/all_links.txt>`__.

It is not recommended to install them individually, because Snakemake
will use conda internally to install the different environments included
in this repository. This list is just for reference purposes.

Installation
------------

To deploy this project, first you need to install conda, get the
pipeline, and install snakemake.

1. Get conda
~~~~~~~~~~~~

You don’t need to run it if you already have a working ``conda``
installation. If you don’t have ``conda`` follow the steps below to
install it in the local directory ``conda-install``.

.. code:: bash

    curl --output Miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda.sh -b -p conda-install
    source conda-install/etc/profile.d/conda.sh
    conda install mamba --channel conda-forge --yes

2. Get the pipeline and install snakemake
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   git clone https://github.com/HI-FRIENDS-SDC2/hi-friends
   cd hi-friends
   mamba env create -f environment.yml
   conda activate snakemake

Now you can execute the pipeline in different ways:

(a) Test workflow execution.

::

   python run.py --check

(b) Execution of the workflow for *Hi-Friends*. You may want to modify
    the contents of ``config/config.yaml``:

::

   python run.py 

You can also run the unit tests to verify each individual step:

::

   python -m pytest .tests/unit/

Deploy in containers
--------------------

Docker
~~~~~~

To run the workflow with the Docker container system you need to do the
following steps:

Build the workflow image
^^^^^^^^^^^^^^^^^^^^^^^^

1. Clone the respository from this ``github`` repository:

::

   git clone https://github.com/HI-FRIENDS-SDC2/hi-friends.git

2. Change to the created directory:

::

   cd hi-friends

3. Now build the image. For this we build and tag the image as
   ``hi-friends-wf``:

::

   docker build -t hi-friends-wf -f deploy.docker .

Run the workflow
^^^^^^^^^^^^^^^^

4. Now we can run the container and then workflow:

::

   docker run -it hi-friends-wf

Once inside the container:

(a) Test workflow execution.

::

   python run.py --check

(b) Execution of the workflow for *Hi-Friends*. You may want to modify
    the contents of ``config/config.yaml``:

::

   python run.py 

Singularity
~~~~~~~~~~~

To run the workflow with singularity you can bild the image from our
repository:

Build the image:
^^^^^^^^^^^^^^^^

1. Clone the respository from this ``github`` repository:

::

   git clone https://github.com/HI-FRIENDS-SDC2/hi-friends.git

2. Change to the created directory:

::

   cd hi-friends

3. Build the Hi-Friends workflow image:

::

   singularity build --fakeroot hi-friends-wf.sif deploy.singularity

.. _run-the-workflow-1:

Run the workflow
^^^^^^^^^^^^^^^^

Once this is done, you can now launch the workflow as follows

::

   singularity shell --cleanenv --bind $PWD hi-friends-wf.sif 

And now, set the environment and activate it:

::

   source /opt/conda/etc/profile.d/conda.sh
   conda activate snakemake

and now, run the Hi-Friends workflow:

(a) Test workflow execution.

::

   python run.py --check

(b) Execution of the workflow for *Hi-Friends*. You may want to modify
    the contents of ``config/config.yaml``:

::

   python run.py 

Podman
~~~~~~

To run the workflow with podman you can build the image from our
repository using our dockerfile:

.. _build-the-image-1:

Build the image:
^^^^^^^^^^^^^^^^

1. Clone the respository from this ``github`` repository:

::

   git clone https://github.com/HI-FRIENDS-SDC2/hi-friends.git

2. Change to the created directory:

::

   cd hi-friends

3. Build the Hi-Friends workflow image:

::

   podman build -t hi-friends-wf -f deploy.docker .

4. Run the workflow:

::

   podman  run  -it hi-friends-wf

.. _run-the-workflow-2:

Run the workflow
^^^^^^^^^^^^^^^^

Once inside the container:

(a) Test workflow execution.

::

   python run.py --check

(b) Execution of the workflow for *Hi-Friends*. You may want to modify
    the contents of ``config/config.yaml``:

::

   python run.py 
