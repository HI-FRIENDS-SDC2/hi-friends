[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8F%20%20%E2%97%8B-orange)](https://fair-software.eu)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/HI-FRIENDS-SDC2/hi-friends/HEAD?urlpath=lab/tree/docs/source/_static/mybinder_execution.ipynb)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
[![Documentation Status](https://readthedocs.org/projects/hi-friends-sdc2/badge/?version=latest)](https://hi-friends-sdc2.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5167659.svg)](https://doi.org/10.5281/zenodo.5167659)

## Summary

This repository hosts a workflow to process HI data cubes produced by radio interferometers, in particular large data cubes produced by future instruments like the [SKA](https://www.skatelescope.org/). It extract radio sources and characterize their main properties. 

The workflow is managed and executed using [snakemake](https://snakemake.readthedocs.io/en/stable/) workflow management system. It uses `spectral-cube` based on `dask` parallelization tool and `astropy` suite to divide the large cube in smaller pieces. On each of the subcubes, we execute [Sofia-2](https://github.com/SoFiA-Admin/SoFiA-2) for masking the subcubes, find sources and characterize their properties. Finally, the individual catalogs are cleaned, concatenated into a single catalog, and duplicates from the overlapping regions are eliminated. Some diagnostic plots are produced using Jupyter notebook.

## HI-FRIENDS team: participation in the SKA Data Challenge 2

This repository contains the workflow used to find and characterize the HI sources in the data cube of the [SKA Data Challenge 2](https://sdc2.astronomers.skatelescope.org/). This is developed by the HI-FRIENDS team. The execution of the workflow was conducted in the [SP-SRC](https://spsrc-user-docs.readthedocs.io/en/latest/) cluster at the [IAA-CSIC](https://www.iaa.csic.es/en/). Documentation can be found in [HI-FRIENDS SDC2 Documentation](https://hi-friends-sdc2.readthedocs.io/en/latest/) (more details below).

## Accessibility to the workflow

Following [FAIR principles](https://www.go-fair.org/fair-principles/), we are trying to make the workflow as accessible as possible. The contents of this repository and the solution to participate in the SDC2 are published in this [Zenodo record](https://zenodo.org/badge/latestdoi/385866513). The snakemake workflow is also provided as a singularity and a docker container. The workflow is also published in [WorkflowHub](https://workflowhub.eu/workflows/141). [Installation](https://hi-friends-sdc2.readthedocs.io/en/latest/installation.html) and [execution](https://hi-friends-sdc2.readthedocs.io/en/latest/execution.html) instructions can be found in the online documentation developed in this repository.

## Installing

For details on installing and using HI-FRIENDS, please visit the documentation: [installation](https://hi-friends-sdc2.readthedocs.io/en/latest/installation.html), [execution](https://hi-friends-sdc2.readthedocs.io/en/latest/execution.html).

## License

We are using GNU General Public License v3.0. See full license [here](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/LICENSE).
![image](https://user-images.githubusercontent.com/1053066/128527855-268a552d-108d-4920-9067-358098eb8f24.png)

## Citation

Please, use this reference (resolves to most recent version in Zenodo): https://doi.org/10.5281/zenodo.5167659


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


## Contributing

More details in [CONTRIBUTING.MD](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/CONTRIBUTING.md). Summary here:

### Coding

Nothing fancy here, just:

1. Fork this repo
1. Commit you code
1. Submit a pull request. It will be reviewed by maintainers and they'll give you proper feedback so you can iterate over it.

#### Considerations
- Make sure existing tests pass
- Make sure your new code is properly tested and fully-covered
- Following [The seven rules of a great Git commit message](https://chris.beams.io/posts/git-commit/#seven-rules) is highly encouraged
- When adding a new feature, branch from [master-branch](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master)


### Testing

As mentioned above, existing tests must pass and new features are required to be tested and fully-covered.

### Documenting

Code should be self-documented. But, in case there is any code that may be hard to understand, it must include some comments to make it easier to review and maintain later on.
