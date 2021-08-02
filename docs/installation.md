# Workflow installation 

## Dependencies

The requirements of the workflow are self-contained, and they will be retrieved and installed during execution using `conda`. To run the pipeline you need to have [snakemake](https://snakemake.readthedocs.io/en/stable/) installed. This can be obtained from the `environment.yml` file in the repository as explained in the next Section. The workflow uses the following packages:

  - astropy=4.2.1
  - astroquery=0.4.1
  - astroquery=0.4.3
  - dask=2021.3.1
  - gitpython=3.1.18
  - ipython=7.22.0
  - ipython=7.25.0
  - jinja2=3.0.1
  - jupyter=1.0.0
  - jupyterlab=3.0.16
  - jupyterlab_pygments=0.1.2
  - matplotlib=3.3.4
  - matplotlib=3.4.2
  - msgpack-python=1.0.2
  - networkx=2.6.1
  - numpy=1.20.1
  - numpy=1.20.3
  - numpy=1.21.1
  - pandas=1.2.2
  - pandas=1.2.5
  - pandas=1.3.0
  - pip=21.0.1
  - pygments=2.9.0
  - pygraphviz=1.7
  - python-wget=3.2
  - python=3.8.6
  - python=3.9.6
  - pyyaml=5.4.1
  - scipy=1.7.0
  - seaborn=0.11.1
  - snakemake-minimal=6.6.1
  - sofia-2=2.3.0
  - spectral-cube=0.5.0
  - wget=1.20.1

It is not recommended to install them individually, because Snakemake will use conda internally to install the different environments included in this repository. This list is just for reference purposes.


## Installation

To deploy this project, first you need to install conda, get the pipeline, and install snakemake. 


### 1. Get conda

You don't need to run it if you already have a working `conda` installation. If you don't have `conda` follow the steps below to install it in the local directory `conda-install`.

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


## Deploy in containers

### Docker

To run the workflow with the Docker container system you need to do the following steps:

#### Build the workflow image

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
docker build -t hi-friends-wf -f deploy.docker
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

(b) Execution of the workflow for *Hi-Friends*:

```
python run.py 
```


### Singularity

To run the workflow with singularity you can bild the image from our repository:

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
singularity build hi-friends-wf.sif hi-friends-wf.def
```

#### Run the workflow

Once this is done, you can now launch the workflow as follows

```
singularity shell --cleanenv hi-friends-wf.sif 
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

(b) Execution of the workflow for *Hi-Friends*:

```
python run.py 
```
