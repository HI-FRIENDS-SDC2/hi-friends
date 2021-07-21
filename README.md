# SKA Data Challenge 2 participation of the team HI-FRIENDS

# Installation

First you need to install conda, get the pipeline, and install snakemake. 
1. Get conda

You don't need to run it if you already have a working `conda` installation. If you don't have `conda` follow the steps below to install it in the local directory `conda-install`.

```bash
 curl --output Miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
 bash Miniconda.sh -b -p conda-install
 source conda-install/etc/profile.d/conda.sh
 conda install mamba --channel conda-forge --yes
```

2. Get the pipeline and install snakemake

```bash
git clone https://github.com/HI-FRIENDS-SDC2/hi-friends
cd hi-friends
mamba env create -f environment.yml
conda activate snakemake
```

3. Execute the pipeline

Follow these commands to run the pipeline on a small dataset to verify everything works:
```bash
python run.py --check
```

First, this will create all the conda environments needed for the different stages of the pipeline. Then, they will be executed.

To execute the pipeline on your own dataset, first remove the directories `results` and `interim` if you have created them. You may want to edit `config/config.yml` to define your configuration, including the dataset to process. Run the pipeline with:
```bash
python run.py
```
