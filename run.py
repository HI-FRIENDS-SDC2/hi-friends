import os
import shutil
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

def rmdir(pathdir, message='Deleted:'):
    if os.path.exists(pathdir):
        try:
            shutil.rmtree(pathdir)
            #logger.info('{0} {1}'.format(message, pathdir))
        except:
            #logger.debug('Could not delete: {0} {1}'.format(message, pathdir))
            pass

def rmfile(pathdir, message='Deleted:'):
    if os.path.exists(pathdir):
        try:
            os.remove(pathdir)
            #logger.info('{0} {1}'.format(message, pathdir))
        except:
            #logger.debug('Could not delete: {0} {1}'.format(message, pathdir))
            pass

def run_summary():
    print('Now producing summary plots and report')
#    os.system("snakemake --rulegraph | dot -Tsvg > images/rulegraph.svg")
#    os.system("snakemake --dag | dot -Tsvg > images/dag.svg")
    os.system("snakemake --report results/report.html")

def run_check():
    url = 'https://github.com/SoFiA-Admin/SoFiA-2/wiki/documents/sofia_test_datacube.tar.gz'
    if not os.path.isdir('interim'):
        os.mkdir('interim')
    if not os.path.isfile('interim/sofia_test_datacube.fits'):
        wget.download(url, 'interim/')
        os.system('cd interim && tar xvfz sofia_test_datacube.tar.gz; cd ..')
    # Execute pipeline on test dataset
    os.system("snakemake -j8 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --config incube='interim/sofia_test_datacube.fits' subcube_id=[0,1,2,3] num_subcubes=4 pixel_overlap=0")
    rmdir('tmp')
    run_summary()

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
    rmdir('tmp')
    run_summary()
    

if __name__ == '__main__':
    main()


