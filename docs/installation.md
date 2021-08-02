# Workflow installation 

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
