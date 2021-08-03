# The HI-FRIENDS solution of the SKA Data Challenge 2 

These pages contain the documentation related to the software developed by the HI-FRIENDS team to analyse SKA simulated data to participate in [the second SKA Science Data Challenge (SDC2)](https://sdc2.astronomers.skatelescope.org/). The SDC2 is a source finding and source characterisation data challenge to find and characterise the neutral hydrogen content of galaxies across a sky area of 20 square degrees. 

HI-FRIENDS has implemented a scientific workflow for accomplishing the SDC2. This workflow and the associated scripts have been published in a gitHub repository, including also the software environments and other elements (i.e. conda environments, docker containers or jupyter notebooks) to facilitate its re-execution.

The software is published in a GitHub repository (see below). It is intended for SKA community members interested to know about the software analysis that will be performed on the SKA data. This documentation aims at assisting these scientists to understand, re-use the published scientific workflow as well as to verify it.  


## Software general description and where is stored 

The [HI-FRIENDS github repository](https://github.com/HI-FRIENDS-SDC2/hi-friends) contains the workflow used to find and characterize the HI sources in the data cube of the SKA Data Challenge 2. This is developed by the HI-FRIENDS team. The execution of the workflow was conducted in the SKA Regional Centre Prototype cluster at the IAA-CSIC (Spain).

The workflow is managed and executed using [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow management system. It uses `spectral-cube` based on `dask` parallelization tool and `astropy` suite to divide the large cube in smaller pieces. On each of the subcubes, we execute [Sofia-2](https://github.com/SoFiA-Admin/SoFiA-2) for masking the subcubes, find sources and characterize their properties. Finally, the individual catalogs are cleaned, concatenated into a single catalog, and duplicates from the overlapping regions are eliminated. Some diagnostic plots are produced using Jupyter notebook.


## Participants 

- Mohammad Akhlaghi
- Antxon Alberdi
- John Cannon
- Laura Darriba
- José Francisco Gómez
- Julián Garrido
- Josh Gósza
- Diego Herranz
- Mike Jones
- Peter Kamphuis
- Dane Kleiner
- Isabel Márquez
- Javier Moldón
- Mamta Pandey-Pommier
- Pepe Sabater
- Susana Sánchez
- Amidou Sorgho
- Lourdes Verdes-Montenegro
