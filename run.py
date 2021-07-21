import os
import argparse
import wget
import psutil

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Select dataset'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c', '--cpus', dest='cpus', help='Number of CPUs available to the pipeline. Default is to use all', default=0)
    parser.add_argument('--check', action='store_true', help='Run quick execution with a test dataset to verify that everything is installed correctly', default=False)
    args = parser.parse_args()
    return args

def run_check():
    if not os.path.isdir('interim'):
        os.mkdir('interim')

    url = 'https://github.com/SoFiA-Admin/SoFiA-2/wiki/documents/sofia_test_datacube.tar.gz'
    wget.download(url, 'interim/')
    os.system("snakemake -j1 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --config incube='/mnt/scratch/sdc2/data/minimal/sofia_test_datacube.fits' subcube_id=[0,1,2,3] num_subcubes=4 pixel_overlap=0")

def main():
    args = get_args()
    if args.check:
        run_check()
        exit(0)
    # Normal execution
    if args.cpus == 0:
        cpus = psutil.cpu_count()
    else:
        cpus = args.cpus
    os.system(f'snakemake -j{cpus} --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1')

if __name__ == '__main__':
    main()


