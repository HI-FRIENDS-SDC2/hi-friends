FROM ubuntu:20.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget git curl apt-utils && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

RUN conda install mamba --channel conda-forge --yes

RUN /bin/bash -c "source /root/miniconda3/etc/profile.d/conda.sh" 

RUN mkdir /hi-friends

COPY . /hi-friends

RUN cd hi-friends && mamba env create -f environment.yml 

RUN conda init bash
RUN echo "conda activate snakemake" >> /root/.bashrc
RUN echo "cd /hi-friends/" >> /root/.bashrc

WORKDIR /hi-friends
