# SDC2 Reproducibility award

In this section we provide links for earch item in the reproducibility award check list.


## Reproducibility of the solution check list  

Well-documented 

- [X] High-level description of what/who the software is for is available [the HI-FRIENDS solution to the SDC2](https://hi-firends-sdc2.readthedocs.io/en/latest/#the-hi-friends-solution-to-the-sdc2)
- [X] High-level description of what the software does is available [software general description](https://hi-firends-sdc2.readthedocs.io/en/latest/#workflow-general-description)
- [X] High-level description of how the software works is available [workflow](https://hi-friends-sdc2.readthedocs.io/en/latest/workflow/)
- [ ] Documentation consists of clear, step-by-step instructions [workflow installation](https://hi-firends-sdc2.readthedocs.io/en/latest/installation/) [execution](https://hi-firends-sdc2.readthedocs.io/en/latest/execution/) [methodology](https://hi-firends-sdc2.readthedocs.io/en/latest/methodology/)
- [ ] Documentation gives examples of what the user can see at each step e.g. screenshots or command-line excerpt
- [ ] Documentation uses monospace fonts for command-line inputs and outputs, source code fragments, function names, class names etc
- [X] Documentation is held under version control alongside the code [repository](https://github.com/HI-FRIENDS-SDC2/hi-friends)

Easy to install 

- [ ] Full instructions provided for building and installing any software [worklow installation]((https://hi-firends-sdc2.readthedocs.io/en/latest/installation/))
- [ ] All dependencies are listed, along with web addresses, suitable versions, licences and whether they are mandatory or optional  [worklow installation]((https://hi-firends-sdc2.readthedocs.io/en/latest/installation/))
- [ ] All dependencies are available 
- [ ] Tests are provided to verify that the installation has succeeded []()
- [ ] A containerised package is available, containing the code together with all of the related configuration files, libraries, and dependencies required. Using e.g. Docker/Singularity [docker]()

Easy to use 

- [ ] A getting started guide is provided outlining a basic example of using the software e.g. a README file
- [ ] Instructions are provided for many basic use cases
- [ ] Reference guides are provided for all command-line, GUI and configuration options

Open licence 

- [X] Software has an open source licence e.g. GNU General Public License (GPL), BSD 3-Clause [license](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/LICENSE)
- [X] License is stated in source code repository [license](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/LICENSE)
- [X] Each source code file has a licence header [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)

Have easily accessible source code

- [X] Access to source code repository is available online [repository](https://github.com/HI-FRIENDS-SDC2/hi-friends)
- [X] Repository is hosted externally in a sustainable third-party repository e.g. SourceForge, LaunchPad, GitHub: Introduction to GitHub [repository](https://github.com/HI-FRIENDS-SDC2/hi-friends)
- [ ] Documentation is provided for developers

Adhere to coding standards 

- [X] Source code is laid out and indented well [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [X] Source code is commented [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [ ] There is no commented out code [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [X] Source code is structured into modules or packages [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [X] Source code uses sensible class, package and variable names [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [ ] Source code structure relates clearly to the architecture or design

Utilise tests 

- [ ] Source code has unit tests
- [ ] Software recommends tools to check conformance to coding standards e.g. A ‘linter’ such as PyLint for Python 



# Examples

## Unit test
The unit tests in the repository verify that the output from the different workflow rules match byte by byte with the outputs expected by the workflow on a small test example. We executed the tests on [myBinder](https://mybinder.org/), which automatically installs all the dependencies. We run this single command and obtained the following output:
```
jovyan@jupyter-hi-2dfriends-2dsdc2-2dhi-2dfriends-2dfsc1x4x2:~$ python -m pytest .tests/unit/
===================================================================================================== test session starts =====================================================================================================
platform linux -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/jovyan
plugins: anyio-2.2.0
collected 6 items                                                                                                                                                                                                             

.tests/unit/test_all.py .                                                                                                                                                                                               [ 16%]
.tests/unit/test_concatenate_catalogs.py .                                                                                                                                                                              [ 33%]
.tests/unit/test_define_chunks.py .                                                                                                                                                                                     [ 50%]
.tests/unit/test_final_catalog.py .                                                                                                                                                                                     [ 66%]
.tests/unit/test_run_sofia.py .                                                                                                                                                                                         [ 83%]
.tests/unit/test_sofia2cat.py .                                                                                                                                                                                         [100%]

================================================================================================ 6 passed in 206.24s (0:03:26) ================================================================================================
```
