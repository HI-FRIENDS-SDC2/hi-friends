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

def run_summary(command):
    print('Now producing summary plots and report')
    if not os.path.isdir('summary'):
        os.mkdir('summary')
    os.system(command + " --report summary/report.html")
    os.system(command + " --rulegraph --forceall | dot -Tsvg > summary/rulegraph.svg")
    os.system(command + " --dag --forceall | dot -Tsvg > summary/dag.svg")
    os.system(command + " --filegraph --forceall | dot -Tsvg > summary/filegraph.svg")

def run_check():
    url = 'https://github.com/SoFiA-Admin/SoFiA-2/wiki/documents/sofia_test_datacube.tar.gz'
    if not os.path.isdir('interim'):
        os.mkdir('interim')
    if not os.path.isfile('interim/sofia_test_datacube.fits'):
        wget.download(url, 'interim/')
        os.system('cd interim && tar xvfz sofia_test_datacube.tar.gz; cd ..')
    # Execute pipeline on test dataset
    command = "snakemake -j8 --use-conda --conda-frontend mamba --default-resources tmpdir=tmp  --resources bigfile=1 --config incube='interim/sofia_test_datacube.fits' subcube_id=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] num_subcubes=4 pixel_overlap=0"
    run_command(command)

def run_command(command):
    print(command)
    os.system(command)
    rmdir('tmp')
    run_summary(command)

def main():
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


