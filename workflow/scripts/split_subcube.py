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
This script splits the cube in different subcubes according to a grid of subcubes
'''

import argparse
import numpy as np
from spectral_cube import SpectralCube
from astropy import units as u

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Split subcube identified by an index'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--index', dest='idx', help='Subcube index')
    parser.add_argument('-d', '--datacube', dest='datacube', \
                        help='Data cube to process.')
    parser.add_argument('-c', '--coord', dest='coord_file', \
                        help='File with edge coordinates of subcubes')
    args = parser.parse_args()
    return args

def split_subcube(infile, coord_subcubes, idx):
    '''Creates a fits file containing the coordinates
    x low x high y low and y high

    Parameters
    ----------
    infile: str
        Input file name
    coord_subcubes: array
        Array containing coordinates of subcubes
    idx: int
        Index of subcube
    '''
    print(f'Now exporting item {idx}')
    print(coord_subcubes[idx])
    cidx = coord_subcubes[idx]

    cube = SpectralCube.read(infile)
    sub_cube = cube.subcube(xlo=cidx[0]*u.deg, xhi=cidx[2]*u.deg,
                            ylo=cidx[1]*u.deg, yhi=cidx[3]*u.deg)
    sub_cube.write(f'interim/subcubes/subcube_{idx}.fits')

def main():
    '''Splits the data cube in several subcubes'''
    args = get_args()
    idx = int(args.idx)
    infile = args.datacube
    coord_subcubes = np.loadtxt(args.coord_file, skiprows=1, delimiter=',')
    coord_subcubes = np.atleast_2d(coord_subcubes)
    split_subcube(infile, coord_subcubes, idx)


if __name__ == '__main__':
    main()
