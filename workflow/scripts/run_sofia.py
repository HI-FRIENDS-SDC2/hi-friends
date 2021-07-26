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
def update_parfile(parfile, output_path, datacube):
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
        fileout.write(lines)
    return updated_parfile

def run_sofia(parfile, outname, datacube, results_path):
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
    Examples
    --------
    ****
    """
    #It makes sense to not run this when the results exist but maybe a check
    #on an existing catalog is better
    output_path = os.path.join(results_path, outname)
    output_catalog = os.path.join(output_path, f'{outname}_{datacube}_cat.txt')
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    if not os.path.isfile(output_catalog):
        #updated_parfile = update_parfile(parfile, output_path, datacube, outname)
        updated_parfile = update_parfile(parfile, output_path, datacube)
        if is_tool('sofia'):
            print('Executing Sofia-2')
            subprocess.call(["sofia", f"{updated_parfile}"])
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
              datacube=args.datacube, results_path=args.results_path)

if __name__ == '__main__':
    main()
