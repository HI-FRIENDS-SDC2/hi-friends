# SDC2 Reproducibility award

In this section we provide links for earch item in the reproducibility award check list.


## Reproducibility of the solution check list  

Well-documented 

- [X] High-level description of what/who the software is for is available [the HI-FRIENDS solution to the SDC2](https://hi-firends-sdc2.readthedocs.io/en/latest/#the-hi-friends-solution-to-the-sdc2)
- [X] High-level description of what the software does is available [software general description](https://hi-firends-sdc2.readthedocs.io/en/latest/#workflow-general-description)
- [X] High-level description of how the software works is available [workflow](https://hi-friends-sdc2.readthedocs.io/en/latest/workflow/)
- [X] Documentation consists of clear, step-by-step instructions [workflow installation](https://hi-firends-sdc2.readthedocs.io/en/latest/installation/) [execution](https://hi-firends-sdc2.readthedocs.io/en/latest/execution/) [methodology](https://hi-firends-sdc2.readthedocs.io/en/latest/methodology/)
- [ ] Documentation gives examples of what the user can see at each step e.g. screenshots or command-line excerpt [execution](https://hi-firends-sdc2.readthedocs.io/en/latest/execution/)
- [ ] Documentation uses monospace fonts for command-line inputs and outputs, source code fragments, function names, class names etc
- [X] Documentation is held under version control alongside the code [repository](https://github.com/HI-FRIENDS-SDC2/hi-friends)

Easy to install 

- [X] Full instructions provided for building and installing any software [worklow installation](https://hi-firends-sdc2.readthedocs.io/en/latest/installation/)
- [X] All dependencies are listed, along with web addresses, suitable versions, licences and whether they are mandatory or optional  [worklow installation]((https://hi-firends-sdc2.readthedocs.io/en/latest/installation/)). List of all required [packages](materials/all_dependencies.txt) and their versions. [Links](materials/all_links.txt) to source code of each dependency including licenses.
- [X] All dependencies are available. [Links](materials/all_links.txt) to source code of each dependency including licenses.
- [X] Tests are provided to verify that the installation has succeeded. [Unit tests](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/.tests/unit), [info unit tests](https://hi-firends-sdc2.readthedocs.io/en/latest/methodology/unit-tests)
- [X] A containerised package is available, containing the code together with all of the related configuration files, libraries, and dependencies required. Using e.g. Docker/Singularity [docker](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/deploy.docker), [singularity](https://github.com/HI-FRIENDS-SDC2/hi-friends/blob/master/deploy.singularity)

Easy to use 

- [X] A getting started guide is provided outlining a basic example of using the software e.g. a README file [Docs: execution](https://hi-firends-sdc2.readthedocs.io/en/latest/installation/)
- [X] Instructions are provided for many basic use cases. [Docs: execution](https://hi-firends-sdc2.readthedocs.io/en/latest/installation/)
- [X] Reference guides are provided for all command-line, GUI and configuration options. [Docs: execution](https://hi-firends-sdc2.readthedocs.io/en/latest/installation/)


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
- [X] There is no commented out code [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [X] Source code is structured into modules or packages [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [X] Source code uses sensible class, package and variable names [source code](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/workflow/scripts)
- [X] Source code structure relates clearly to the architecture or design [workflow](https://hi-friends-sdc2.readthedocs.io/en/latest/workflow/workflow-file-structure)

Utilise tests 

- [X] Source code has unit tests. [Unit tests](https://github.com/HI-FRIENDS-SDC2/hi-friends/tree/master/.tests/unit), [info unit tests](https://hi-firends-sdc2.readthedocs.io/en/latest/methodology/unit-tests)
- [ ] Software recommends tools to check conformance to coding standards e.g. A ‘linter’ such as PyLint for Python. [Pylint verification](https://hi-firends-sdc2.readthedocs.io/en/latest/methodology/check-conformance-to-coding-standards)
