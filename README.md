[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8F%20%20%E2%97%8B-orange)](https://fair-software.eu)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HI-FRIENDS-SDC2/hi-friends/HEAD?urlpath=lab/tree/docs/_static/mybinder_execution.ipynb)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
[![Documentation Status](https://readthedocs.org/projects/hi-friends-sdc2/badge/?version=latest)](https://hi-friends-sdc2.readthedocs.io/en/latest/?badge=latest)

# HI-FRIENDS team: participation in the SKA Data Challenge 2

This repository contains the workflow used to find and characterize the HI sources in the data cube of the [SKA Data Challenge 2](https://sdc2.astronomers.skatelescope.org/). This is developed by the HI-FRIENDS team. The execution of the workflow was conducted in the [SP-SRC](https://spsrc-user-docs.readthedocs.io/en/latest/) cluster at the [IAA-CSIC](https://www.iaa.csic.es/en/).


## Summary

The workflow is managed and executed using [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow management system. It uses `spectral-cube` based on `dask` parallelization tool and `astropy` suite to divide the large cube in smaller pieces. On each of the subcubes, we execute [Sofia-2](https://github.com/SoFiA-Admin/SoFiA-2) for masking the subcubes, find sources and characterize their properties. Finally, the individual catalogs are cleaned, concatenated into a single catalog, and duplicates from the overlapping regions are eliminated. Some diagnostic plots are produced using Jupyter notebook.

The contents of this repository and the solution to participate in the SDC2 are published in Zenodo: TBD

## Documentation

The repository documentation can be found in the [HI-FRIENDS SDC2](https://hi-friends-sdc2.readthedocs.io/en/latest/) webpage where you can find details on:

- The SKA Data Challenge 2
  - The HI-FRIENDS solution to the SDC2
  - Workflow general description
  - The HI-FRIENDS team
- Methodology
  - Data exploration
  - Feedback from the workflow and logs
  - Configuration
  - Unit tests
  - Software managed and containerization
  - Check conformance to coding standards
- Workflow Description
  - Workflow definition diagrams
  - Workflow file structure
  - Output products
  - Snakemake execution and diagrams
- Workflow installation
  - Dependencies
  - Installation
        1. Get conda
        2. Get the pipeline and install snakemake
  - Deploy in containers
        - Docker
        - Singularity
        - Podman
  - Use tarball of the workflow
  - Use myBinder
- Workflow execution
  - Preparation
  - Basic usage and verification of the workflow
  - Execution on a data cube
- SDC2 HI-FRIENDS results
  - Our solution
  - Score
- SDC2 Reproducibility award
  - Reproducibility of the solution check list
- Developers
  - define_chunks module
  - eliminate_duplicates module
  - filter_catalog module
  - run_sofia module
  - sofia2cat module
  - split_subcube module
- Acknowledgments
