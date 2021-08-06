# This file is part of Hi-FRIENDS SDC2
# (https://github.com/HI-FRIENDS-SDC2/hi-friends).
# Copyright (c) 2021 Javier Moldón
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import argparse
import wget
import psutil

def get_args():
    '''This function parses and returns arguments passed in'''
    description = 'Select dataset'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c', '--cpus', dest='cpus', help='Number of CPUs available to the pipeline. Default is to use all', default=0)
    parser.add_argument('--check', action='store_true', help='Run quick execution with a test dataset to verify that everything is installed correctly', default=False)
    args = parser.parse_args()
    return args

def rmdir(pathdir):
    '''Removes directory

    Parameters
    ----------
    pathdir: str
        Path to directory to be removed
    '''
    if os.path.exists(pathdir):
        try:
            shutil.rmtree(pathdir)
        except:
            pass

def rmfile(pathdir):
    '''Removes file

    Parameters
    ----------
    pathdir: str
        Path to file to be removed
    '''
    if os.path.exists(pathdir):
        try:
            os.remove(pathdir)
        except:
            pass

def run_summary(command):
    '''Generates snakemake diagram plots

    Parameters
    ----------
    command: str
        Command used for the snakemake execution
    '''
    print('Now producing summary plots and report')
    if not os.path.isdir('summary'):
        os.mkdir('summary')
    os.system(command + " --report summary/report.html")
    os.system(command + " --rulegraph --forceall | dot -Tsvg > summary/rulegraph.svg")
    os.system(command + " --dag --forceall | dot -Tsvg > summary/dag.svg")
    os.system(command + " --filegraph --forceall | dot -Tsvg > summary/filegraph.svg")

def run_check():
    '''Executes the snakemake workflow in check mode'''
    url = 'https://github.com/SoFiA-Admin/SoFiA-2/wiki/documents/sofia_test_datacube.tar.gz'
    if not os.path.isdir('interim'):
        os.mkdir('interim')
    if not os.path.isfile('interim/sofia_test_datacube.fits'):
        wget.download(url, 'interim/')
        os.system('cd interim && tar xvfz sofia_test_datacube.tar.gz; cd ..')
    # Execute pipeline on test dataset
    command = "snakemake -j8 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --config incube='interim/sofia_test_datacube.fits' sofia_param='config/dev12.par' subcube_id=[0] num_subcubes=16 pixel_overlap=0"
    run_command(command)

def run_command(command):
    '''Executes a shell command, removes `tmp` dir and runs summary

    Parameters
    ----------
    command: str
        Command used for the snakemake execution
    '''
    print(command)
    os.system(command)
    rmdir('tmp')
    run_summary(command)

def main():
    '''Executes snakemake workflow'''
    args = get_args()
    if args.check:
        run_check()
    elif not args.check:
        # Normal execution
        if args.cpus == 0:
            cpus = psutil.cpu_count()
        else:
            cpus = args.cpus
        command = f'snakemake -j{cpus} --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1'
        run_command(command) 

if __name__ == '__main__':
    main()


