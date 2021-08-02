In this section we provide a description of the software used and where is stored, in particular we provide a high-level description of what the software is for, high-level description of what the software does, installation instructions with dependencies list and examples of how to run the workflow.   


# Software general description and where is stored 

The [HI-FRIENDS github repository](https://github.com/HI-FRIENDS-SDC2/hi-friends) contains the workflow used to find and characterize the HI sources in the data cube of the SKA Data Challenge 2. This is developed by the HI-FRIENDS team. The execution of the workflow was conducted in the SP-SRC cluster at the IAA-CSIC.

The workflow is managed and executed using [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow management system. It uses `spectral-cube` based on `dask` parallelization tool and `astropy` suite to divide the large cube in smaller pieces. On each of the subcubes, we execute [Sofia-2](https://github.com/SoFiA-Admin/SoFiA-2) for masking the subcubes, find sources and characterize their properties. Finally, the individual catalogs are cleaned, concatenated into a single catalog, and duplicates from the overlapping regions are eliminated. Some diagnostic plots are produced using Jupyter notebook.



# Participants 


- Mohammad Akhlaghi
- Antxon Alberdi
- John Cannon
- Ancor Damas
- Laura Darriba
- José Francisco Gómez
- Julián Garrido
- Josh Gósza
- Diego Herranz
- Mike Jones
- Peter Kamphuis
- Dane Kleiner
- Sebastián Luna
- Isabel Márquez
- Javier Moldón
- Mamta Pandey-Pommier
- Javier Román
- Pepe Sabater
- Susana Sánchez
- Amidou Sorgho
- Lourdes Verdes-Montenegro



## Acknowledgments

Here we list the credits and acknowledgments for the members of the team.

This work used the SKA Regional Centre Prototype at IAA-CSIC, which is funded by the State Agency for Research of the Spanish MCIU through the "Center of Excellence Severo Ochoa" award to the Instituto de Astrofísica de Andalucía (SEV-2017-0709), the European Regional Development Funds (EQC2019-005707-P), by the Junta de Andalucía (SOMM17_5208_IAA), project RTI2018-096228-B-C31(MCIU/AEI/FEDER,UE) and PTA2018-015980-I(MCIU,CSIC).
