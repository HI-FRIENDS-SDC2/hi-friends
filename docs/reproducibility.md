# Reproducibility

Here we describe our approach to make the solution reproducible and we can include the reproducibility of the solution check list.


## Reproducibility of the solution check list  

Well-documented 

- [ ] High-level description of what/who the software is for is available
- [ ] High-level description of what the software does is available
- [ ] High-level description of how the software works is available
- [ ] Documentation consists of clear, step-by-step instructions
- [ ] Documentation gives examples of what the user can see at each step e.g. screenshots or command-line excerpt
- [ ] Documentation uses monospace fonts for command-line inputs and outputs, source code fragments, function names, class names etc
- [X] Documentation is held under version control alongside the code [repository](https://github.com/HI-FRIENDS-SDC2/hi-friends)

Easy to install 

- [ ] Full instructions provided for building and installing any software
- [ ] All dependencies are listed, along with web addresses, suitable versions, licences and whether they are mandatory or optional
- [ ] All dependencies are available
- [ ] Tests are provided to verify that the installation has succeeded
- [ ] A containerised package is available, containing the code together with all of the related configuration files, libraries, and dependencies required. Using e.g. Docker/Singularity

Easy to use 

- [ ] A getting started guide is provided outlining a basic example of using the software e.g. a README file
- [ ] Instructions are provided for many basic use cases
- [ ] Reference guides are provided for all command-line, GUI and configuration options

Open licence 

- [ ] Software has an open source licence e.g. GNU General Public License (GPL), BSD 3-Clause
- [ ] Licence is stated in source code repository
- [ ] Each source code file has a licence header

Have easily accessible source code

- [ ] Access to source code repository is available online
- [ ] Repository is hosted externally in a sustainable third-party repository e.g. SourceForge, LaunchPad, GitHub: Introduction to GitHub
- [ ] Documentation is provided for developers

Adhere to coding standards 

- [ ] Source code is laid out and indented well
- [ ] Source code is commented
- [ ] There is no commented out code
- [ ] Source code is structured into modules or packages
- [ ] Source code uses sensible class, package and variable names
- [ ] Source code structure relates clearly to the architecture or design

Utilise tests 

- [ ] Source code has unit tests
- [ ] Software recommends tools to check conformance to coding standards e.g. A ‘linter’ such as PyLint for Python



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


