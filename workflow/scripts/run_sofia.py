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

'''
This script runs Sofia *******
'''
import sys
import os
import argparse
import subprocess
from shutil import which
#import yaml

# Functions
def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Select dataset'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--parfile', dest='parfile', \
                        help='Link to Sofia-2 paramenters file', \
                        default='parameters/sofia_01.par')
    parser.add_argument('-r', '--results_path', dest='results_path', \
                        help='Directory for results', default='results')
    parser.add_argument('-o', '--outname', dest='outname', help='Name of output\
                        directory for Sofia products', default='test')
    parser.add_argument('-d', '--datacube', dest='datacube', help='Data cube to\
                        process. Options are: development, development_large, \
                        evaluation', default='development')
    parser.add_argument('-s', '--scfind_threshold', dest='scfind_threshold',
                        help='Define scfind.threshold parameter', default=4.5)
    parser.add_argument('-f', '--reliability_fmin', dest='reliability_fmin',
                        help='Define reliability_fmin parameter', default=6)
    parser.add_argument('-t', '--reliability_threshold', dest='reliability_threshold',
                        help='Define reliability_threshold parameter', default=0.4)
    args = parser.parse_args()
    return args

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None

#def read_config_parameter(configfile, parameter):
#    with open(configfile) as f:
#        data = yaml.load(f, Loader=yaml.FullLoader)
#    return data[parameter]

#def update_parfile(parfile, output_path, datacube, outname):
def update_parfile(parfile, output_path, datacube,
              scfind_threshold, reliability_fmin,
              reliability_threshold):
    '''Updates file with paramenters
    Parameters
    ----------
    parfile: str****
        File contanining parameters
    output_path: str
        Path of output file ****
    datacube: ****
        Data. Data cube
    outname: str
        Name of output file
    Returns
    -------
    updated_parfile: ****
        File with updated parameters
    Examples
    --------
    ****
    '''
    updated_parfile = os.path.join(output_path, 'sofia.par')
#    configfile = 'config/config.yml'
#    datacube_path = read_config_parameter(configfile, datacube)
    datacube_path = datacube
    datacube_name = os.path.basename(datacube).rstrip('.fits')
    with open(parfile, 'r') as filein, open(updated_parfile, 'w') as fileout:
        lines = filein.read().replace('output_path', output_path)
#        lines= lines.replace('outname', f'{outname}_{datacube_name}')
        lines= lines.replace('outname', f'{datacube_name}')
        lines= lines.replace('datacube', datacube_path)
        lines= lines.replace('scfind_threshold', scfind_threshold)
        lines= lines.replace('reliability_fmin', reliability_fmin)
        lines= lines.replace('reliability_threshold', reliability_threshold)
        fileout.write(lines)
    return updated_parfile

def eliminate_time(cat):
    # Read in the file
    with open(cat, 'r') as infile :
      lines = infile.readlines()
    
    # Replace the target string
    for i, line in enumerate(lines):
        if line[:7] == '# Time:':
            lines[i] = '# Time:\n'

    # Write the file out again
    with open(cat, 'w') as infile:
        for i in lines:
            infile.write(i)

def run_sofia(parfile, outname, datacube, results_path,
              scfind_threshold, reliability_fmin,
              reliability_threshold):
    """Only runs Sofia if the output catalog  does not exist
    Parameters
    ----------
    parfile: str****
        File contanining parameters
    outname: str
        Name of output file
    datacube: ****
        Data. Data cube
    results_path: str
        Path to save results
    scfind_threshold: float
        Sofia parameter scfind_threshold
    reliability_fmin: float
        Sofia parameter reliability_fmin
    reliability_threshold: float
        Sofia parameter reliability_threshold
    Examples
    --------
    ****
    """
    #It makes sense to not run this when the results exist but maybe a check
    #on an existing catalog is better
    output_path = os.path.join(results_path, outname)
    datacube_name = os.path.basename(datacube).replace('.fits','')
    output_catalog = os.path.join(output_path, f'{datacube_name}_cat.txt')
    print('AAA', output_catalog)
    print(results_path)
    print(outname)
    print(output_path)
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    if not os.path.isfile(output_catalog):
        #updated_parfile = update_parfile(parfile, output_path, datacube, outname)
        updated_parfile = update_parfile(parfile, output_path, datacube,
              scfind_threshold, reliability_fmin,
              reliability_threshold)
        if is_tool('sofia'):
            print('Executing Sofia-2')
            subprocess.call(["sofia", f"{updated_parfile}"])
            eliminate_time(output_catalog)
        else:
            print('sofia not available. Please install Sofia-2')
            sys.exit(1)
    else:
        print(f"We have already found the catalogue {output_catalog}. \
                Sofia will not be executed" )

def main():
    ''' Runs Sofia if the output catalog does not exist'''
    args = get_args()
    if not os.path.isdir(args.results_path):
        os.mkdir(args.results_path)
    run_sofia(parfile=args.parfile, outname=args.outname,
              datacube=args.datacube, results_path=args.results_path,
              scfind_threshold=args.scfind_threshold,
              reliability_fmin=args.reliability_fmin,
              reliability_threshold=args.reliability_threshold)

if __name__ == '__main__':
    main()
