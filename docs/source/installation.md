# Workflow installation 

This sections starts with the list of the main software used by the workflow, and a detailed list of all the dependencies required to execute it. Please, note that it is not needed to install these dependencies because the workflow will that automatically. The instructions below descripbe how to install the workflow locally (just by installing [snakemake](https://snakemake.readthedocs.io/en/stable/) with [conda](https://docs.conda.io/en/latest/), and snakemake will take care of all the rest). There are also instructions to use the containerized version of the workflow, using either docker, singularity or podman. The possible ways to deploy and use the workflow are:

- Use conda to install snakemake through the `environment.yml`.
- Build or download the docker container.
- Build or download the singularity container.
- Build or download the podman container.
- Download the full tarball of the workflow (includes files of all software) in a Linux machine.
- Open the Github repository in [myBinder](https://mybinder.org/).

## Dependencies

The main software dependencies used for the analysis are: 
 
- [Sofia-2](https://github.com/SoFiA-Admin/SoFiA-2/) (version 2.3.0) which is licensed under the [GNU General Public License v3.0](https://github.com/SoFiA-Admin/SoFiA-2/blob/master/LICENSE)
- [Conda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) (version 4.9.2) which is released under the [3-clause BSD license](https://docs.conda.io/en/latest/license.html)
- [Snakemake](https://snakemake.readthedocs.io/en/stable/) (snakemake-minimal version 6.5.3) which is licensed under the [MIT License](https://snakemake.readthedocs.io/en/stable/project_info/license.html)  
- [Spectral-cube](https://spectral-cube.readthedocs.io/en/latest/installing.html#installation)(version 0.5.0) which is licensed under a [BSD 3-Clause license](https://github.com/radio-astro-tools/spectral-cube/blob/master/LICENSE.rst)
- [Astropy](https://www.astropy.org)(version 4.2.1) which is licensed under a [3-clause BSD style license](https://docs.astropy.org/en/stable/license.html?highlight=license#astropy-license)


The requirements of the HI-FRIENDS data challenge solution workflow are self-contained, and they will be retrieved and installed during execution using `conda`. To run the pipeline you only need to have [snakemake](https://snakemake.readthedocs.io/en/stable/) installed. This can be obtained from the `environment.yml` file in the repository as explained in the [installation instructions](https://hi-friends-sdc2.readthedocs.io/en/latest/installation.html#get-the-pipeline-and-install-snakemake).

The workflow uses the following packages:

```
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
```

This list can also be found in [all dependencies](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/docs/materials/all_dependencies.txt). The links where all the software can be downloaded is in [all links](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/docs/materials/all_links.txt).

It is not recommended to install them individually, because [Snakemake](https://snakemake.readthedocs.io/en/stable/) will use `conda` internally to install the different environments included in this repository. This list is just for reference purposes.


## Installation

To deploy this project, first you need to install conda, get the pipeline, and install snakemake. 


### 1. Get conda

You don't need to run this if you already have a working `conda` installation. If you don't have `conda` follow the steps below to install it in the local directory `conda-install`. We will use the light-weight version `miniconda`. We also install `mamba`, which is a very fast dependency solver for conda. 

```bash
 curl --output Miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
 bash Miniconda.sh -b -p conda-install
 source conda-install/etc/profile.d/conda.sh
 conda install mamba --channel conda-forge --yes
```


### 2. Get the pipeline and install snakemake

```bash
git clone https://github.com/HI-FRIENDS-SDC2/hi-friends
cd hi-friends
mamba env create -f environment.yml
conda activate snakemake
```
Now you can execute the pipeline in different ways:

(a) Test workflow execution.

```
python run.py --check
```

(b) Execution of the workflow for *Hi-Friends*. You will need to modify the contents of `config/config.yaml`:

```
python run.py 
```

You can also run the unit tests to verify each individual step:

```
python -m pytest .tests/unit/
```


## Deploy in containers

### Docker

To run the workflow with the Docker container system you need to do the following steps:

#### Download or Build the workflow image

##### Build the image

1. Clone the respository from this ``github`` repository:

```
git clone https://github.com/HI-FRIENDS-SDC2/hi-friends.git
```

2. Change to the created directory:

```
cd hi-friends
```

3. Now build the image. For this we build and tag the image as ``hi-friends-wf``:

```
docker build -t hi-friends-wf -f deploy.docker .
```

##### Download the image

1. Download the latest image (or choose another version [here](https://zenodo.org/record/5172930)) for docker from Zenodo:

```
wget -O hi-friends-wf.tgz https://zenodo.org/record/5172930/files/hi-friends-wf.tgz?download=1
```

2. Load the image:

```
docker load < hi-friends-wf.tgz
```

#### Run the workflow

4. Now we can run the container and then workflow:

```
docker run -it hi-friends-wf

```

Once inside the container:

(a) Test workflow execution.

```
python run.py --check
```

(b) Execution of the workflow for *Hi-Friends*. You will need to modify the contents of `config/config.yaml`:

```
python run.py 
```


### Singularity

To run the workflow with singularity you can bild the image from our repository:

#### Download or Build the workflow image

##### Download the image

1. Download the latest image (or choose another version [here](https://zenodo.org/record/5172930)) for singularity from Zenodo:

```
wget -O hi-friends-wf.sif https://zenodo.org/record/5172930/files/hi-friends-wf.sif?download=1
```


##### Build the image:

1. Clone the respository from this ``github`` repository:

```
git clone https://github.com/HI-FRIENDS-SDC2/hi-friends.git
```

2. Change to the created directory:

```
cd hi-friends
```

3. Build the Hi-Friends workflow image:

```
singularity build --fakeroot hi-friends-wf.sif deploy.singularity
```

#### Run the workflow

Once this is done, you can now launch the workflow as follows

```
singularity shell --cleanenv --bind $PWD hi-friends-wf.sif 
```

And now, set the environment and activate it:

```
source /opt/conda/etc/profile.d/conda.sh
conda activate snakemake
```

and now, run the Hi-Friends workflow:

(a) Test workflow execution.

```
python run.py --check
```

(b) Execution of the workflow for *Hi-Friends*. You will need to modify the contents of `config/config.yaml`:

```
python run.py 
```


### Podman

To run the workflow with podman you can build the image from our repository using our dockerfile:

#### Build the image:

1. Clone the respository from this ``github`` repository:

```
git clone https://github.com/HI-FRIENDS-SDC2/hi-friends.git
```

2. Change to the created directory:

```
cd hi-friends
```

3. Build the Hi-Friends workflow image:

```
podman build -t hi-friends-wf -f deploy.docker .
```

4. Run the workflow:

```
podman  run  -it hi-friends-wf
```


#### Run the workflow

Once inside the container:

(a) Test workflow execution.

```
python run.py --check
```

(b) Execution of the workflow for *Hi-Friends*. You will need to modify the contents of `config/config.yaml`:

```
python run.py 
```


## Use tarball of the workflow

[This tarball file](https://zenodo.org/record/5167693/files/hi-friends-sdc2-workflow.tar.gz?download=1) is a self-contained workflow archive produced by snakemake containing the code, the config files, and all software packages of each defined conda environment are included. This only works in Linux, tried on Ubuntu 20.04.

You will need to have snakemake installed. You can install it with `conda` using this [environment.yml](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/environment.yml). More information can be found in [above](https://hi-friends-sdc2.readthedocs.io/en/latest/installation.html#get-the-pipeline-and-install-snakemake).

Once you have the tarball and snakemake available, you can do:

```bash
tar -xf hi-friends-sdc2-workflow.tar.gz
conda activate snakemake
snakemake -n
```

## Use myBinder

Simply follow [this link](https://mybinder.org/v2/gh/HI-FRIENDS-SDC2/hi-friends/HEAD?urlpath=lab/tree/docs/_static/mybinder_execution.ipynb). After some time, a virtual machine will be created with all the required software. You will start in a jupyter notebook ready to execute a check of the software. In general, myBinder is not thought to conduct heavy processing, so we recommend to use this option only for verification purposes.
