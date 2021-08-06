# Workflow execution

## Preparation

This is a practical example following the instructions in section [Workflow installation](installation.md). Make sure you have `snakemake` available in your path. You may also be working inside one the proposed containers described in the section.

First we clone the repository.
```bash
$ git clone https://github.com/HI-FRIENDS-SDC2/hi-friends
```
This is what you will see.
![image](https://user-images.githubusercontent.com/1053066/128486786-6476ed77-88e3-4b52-ae10-2fcdb3096283.png)

Now, we access the newly created directory and install the dependencies:
```bash
$ cd hi-friends
$ mamba env create -f environment.yml 
```

![image](https://user-images.githubusercontent.com/1053066/128485995-48f8332d-e37d-4986-b464-43f6d2d8f69c.png)

After a few minutes you will see the confirmation of the creation of the `snakemake` conda environment, which you can activate immediately:
![image](https://user-images.githubusercontent.com/1053066/128487214-e7761e97-e947-45ba-8ea0-29e77533caba.png)

## Basic usage and verification of the workflow

You can check the basic usage of the execution script with:

```bash
$ python run.py -h
```
![image](https://user-images.githubusercontent.com/1053066/128487591-db23279d-c08d-4dc3-a95d-0749c8376ac5.png)

From here you can control how many CPUs to use, and you can enable the `--check` option, which runs the workflow in a small test dataset.

Using the `--check` option produces several stages. First, it automatically downloads a test dataset:
![image](https://user-images.githubusercontent.com/1053066/128487881-f55f27af-097c-47f9-b7b5-ceb41f46650d.png)

Second, `snakemake` is executed with specific parameters to quickly process this test datacube. Before executing the scripts, snakemake will create all the conda environments required for the execution. This operation may take a few minutes:
![image](https://user-images.githubusercontent.com/1053066/128488244-af2b4390-6fe9-40a5-a05d-e585ca857c34.png)

Third, snakemake will build a DAG to describe the execution order of the different steps, and execute them in parallel when possible:
![image](https://user-images.githubusercontent.com/1053066/128488368-0024dbef-6a65-418b-b706-e0d3bfbdc64c.png)

Before each step is started, there is a summary of what will be executed and which conda environment will be used. Two examples at different stages:
![image](https://user-images.githubusercontent.com/1053066/128488614-354b5198-83de-4ad9-baf3-b9180e9fa6f6.png)

![image](https://user-images.githubusercontent.com/1053066/128488761-52481372-2236-4cfe-83de-21c4e56cc39e.png)


After the pipeline is finished, `snakemake` is executed 3 more times to produce the workflow diagrams and an HTML report:
![image](https://user-images.githubusercontent.com/1053066/128488905-d46662ca-fe90-4721-b083-e574b0d499e6.png)

This is how your directory looks after the execution. All the results are stored in `results` following the structure described in [Output products](workflow.html#output-products). The `interim` directory contains subcube fits file, which can be removed to save space.

## Execution on a data cube

If you want to execute the workflow on your own data cube, you have to edit the `config/config.yaml` file. In particular, you must select the path of the datacube using the variable `incube`. 

![image](https://user-images.githubusercontent.com/1053066/128489393-ce26d30e-3aec-4cf2-9b89-497fec686ece.png)

You may leave the other parameters as they are, although it is recommended that you adapt the `sofia_param` file with a Sofia parameters file that works best with your data.

Before re-executing the pipeline, you can clean all the previous products by removing directories `interim` and `results`. If you remove specific files from `results`, snakemake will only execute the required steps to generate the deleted files, but not the ones already existing.

```bash
$ rm -rf results/ interim/
```

You can modify the parameters file and execute `run.py` to run everything directly with `python run.py`. But you can also run `snakemake` with your preferred parameters. In particular, you can parse configuration parameters explicitly in the command line. Let's see some examples:

Execution of the workflow using the configuration file as it is, with default parameters
```bash
snakemake -j32 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp --resources bigfile=1
```

Execution specifying a different data cube:
```bash
snakemake -j32 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp --resources bigfile=1 --config incube='/mnt/scratch/sdc2/data/development/sky_dec_v2.fits' 
```
![image](https://user-images.githubusercontent.com/1053066/128491524-c661cbe0-0dc0-4454-94fa-333e64401534.png)

You could define any of the parameters in the `config.yaml` file as needed. For example:

```bash
snakemake -j32 --use-conda subcube_id=[0,1,2,3] num_subcubes=16 pixel_overlap=4 --config incube='/mnt/scratch/sdc2/data/development/sky_dec_v2.fits' 
```

