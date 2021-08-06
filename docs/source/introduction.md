# The SKA Data Challenge 2

These pages contain the documentation related to the software developed by the HI-FRIENDS team to analyse SKA simulated data to participate in [the second SKA Science Data Challenge (SDC2)](https://sdc2.astronomers.skatelescope.org/). The SDC2 is a source finding and source characterisation data challenge to find and characterise the neutral hydrogen content of galaxies across a sky area of 20 square degrees. 

# The HI-FRIENDS solution to the SDC2

HI-FRIENDS is a team participating in the SDC2. The team has implemented a scientific workflow for processing the 1TB SKA simulated data cube and produce a catalog with the properties of detected sources. This workflow, the required configuration and deployment files and this documentation are maintained with version control with `git` in GitHub to facilitate its re-execution. The software and parameters are optimized for the solution of this challenge, although the workflow can be used to analyse other radio data cubes because the software can deal with cubes from other observatories. The workflow is intended for SKA community members or any astronomer interested in our approach for HI source finding and characterization. This documentation aims at assisting these scientists to understand and re-use the published scientific workflow as well as to verify it.  

The [HI-FRIENDS Github repository](https://github.com/HI-FRIENDS-SDC2/hi-friends) contains the workflow used to find and characterize the HI sources in the data cube of the SKA Data Challenge 2. This is developed by the HI-FRIENDS team. The execution of the workflow was conducted in the [SKA Regional Centre Prototype cluster at the IAA-CSIC (Spain)](https://sdc2.astronomers.skatelescope.org/computational-resources/iaa-csic-proto-src).

## Workflow general description

The workflow is managed and executed using [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow management system. It uses `spectral-cube` based on `dask` parallelization tool and `astropy` suite to divide the large cube in smaller pieces. On each of the subcubes, we execute [Sofia-2](https://github.com/SoFiA-Admin/SoFiA-2) for masking the subcubes, find sources and characterize their properties. Finally, the individual catalogs are cleaned, concatenated into a single catalog, and duplicates from the overlapping regions are eliminated. Some diagnostic plots are produced using Jupyter notebook. Specific details on how the workflows work can be find in the [Workflow](workflow.md) section.


## The HI-FRIENDS team 

- Mohammad Akhlaghi - Instituto de Astrofísica de Canarias
- Antonio Alberdi - Instituto de Astrofísica de Andalucía, CSIC
- John Cannon - Macalester College
- Laura Darriba - Instituto de Astrofísica de Andalucía, CSIC
- José Francisco Gómez - Instituto de Astrofísica de Andalucía, CSIC
- Julián Garrido - Instituto de Astrofísica de Andalucía, CSIC
- Josh Gósza - South African Radio Astronomy Observatory 
- Diego Herranz - Instituto de Física de Cantabria
- Michael G. Jones - The University of Arizona
- Peter Kamphuis - Ruhr University Bochum
- Dane Kleiner - Italian National Institute for Astrophysics
- Isabel Márquez - Instituto de Astrofísica de Andalucía, CSIC
- Javier Moldón - Instituto de Astrofísica de Andalucía, CSIC
- Mamta Pandey-Pommier - Centre  de  Recherche  Astrophysique  de  Lyon,  Observatoire  deLyon
- José Sabater - University of Edinburgh
- Susana Sánchez - Instituto de Astrofísica de Andalucía, CSIC
- Amidou Sorgho - Instituto de Astrofísica de Andalucía, CSIC
- Lourdes Verdes-Montenegro - Instituto de Astrofísica de Andalucía, CSIC
