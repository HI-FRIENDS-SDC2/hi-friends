import sys
import numpy as np
from spectral_cube import SpectralCube
import argparse
from astropy import units as u

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Split subcube identified by an index'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--index', dest='idx', help='Subcube index')
    parser.add_argument('-d', '--datacube', dest='datacube', help='Data cube to process.')
    parser.add_argument('-c', '--coord', dest='coord_file', help='File with edge coordinates of subcubes')
    args = parser.parse_args()
    return args

def split_subcube(infile, coord_subcubes, idx):
    print(f'Now exporting item {idx}')
    print(coord_subcubes[idx])
    c = coord_subcubes[idx]
    
    cube = SpectralCube.read(infile)
    sub_cube = cube.subcube(xlo=c[0]*u.deg, xhi=c[2]*u.deg,
                            ylo=c[1]*u.deg, yhi=c[3]*u.deg)
    #sub_cube.write(f'interim/subcubes/subcube_{idx:02d}.fits')
    sub_cube.write(f'interim/subcubes/subcube_{idx}.fits')

def main():
    args = get_args()
    idx = int(args.idx)
    infile = args.datacube
    coord_subcubes = np.loadtxt(args.coord_file, skiprows=1, delimiter=',')
    coord_subcubes = np.atleast_2d(coord_subcubes)
    split_subcube(infile, coord_subcubes, idx)


if __name__ == '__main__':
    main()



