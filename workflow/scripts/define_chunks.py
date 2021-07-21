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
This script defines the coordintes of grid of subcubes
'''

import argparse
from spectral_cube import SpectralCube
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Define coordinates of grid of subcubes'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--datacube', dest='datacube', \
                        help='Data cube to process.')
    parser.add_argument('-g', '--gridplot', dest='grid_plot', \
                        help='Name of output file to plot the grid of subcubes')
    parser.add_argument('-n', '--num_subcubes', dest='num_subcubes', \
                      help='Total number of subcubes to divide the master cube')
    parser.add_argument('-o', '--overlap', dest='pixel_overlap', \
                        help='Number of pixels to extend the cube in each \
                        direction.')
    args = parser.parse_args()
    return args

def define_subcubes(steps, wcs, overlap, subcube_size_pix):
    '''Return an array with the coordinates of the subcubes
    Parameters
    ----------
    steps: int
        Steps to grid the cube.
    wcs: object
        ****
    overlap: int
        Number of pixels overlaping between subcubes ****
    subcube_size_pix: int
        ****
    Returns
    -------
    coord_subcubes: array
        Array with the coordinates of rthe subcubes
    Examples
    --------
      ****
    '''
    coord_subcubes = []
    for s_x in steps:
        for s_y in steps:
            c_0 = wcs.pixel_to_world(s_x-overlap/2, s_y-overlap/2, 0)[0]
            c_1 = wcs.pixel_to_world(s_x+subcube_size_pix+overlap/2, \
                                    s_y+subcube_size_pix+overlap/2, 0)[0]
            xlo = c_0.ra.deg
            xhi = c_1.ra.deg
            ylo = c_0.dec.deg
            yhi = c_1.dec.deg
            coord_subcubes.append([xlo,ylo, xhi, yhi])
            #print(s_x-overlap/2, s_y-overlap/2, s_x+subcube_size_pix+overlap/2,\
            #      s_y+subcube_size_pix+overlap/2)
            #print(xlo, xhi, ylo, yhi)
    return np.array(coord_subcubes)

def plot_subcubes(coord_subcubes, l_s='-', color=None, l_w=1):
    '''Plot subcubes
    Parameters
    ----------
    coord_subcubes: int
        Steps to grid the cube.
    l_s: *****
        Line style. Defalult value is solid line
    color: ****
        Line color. Default value is no color.
    l_w: ****
        Line width. Default value is 1.
    Returns
    -------
    ****
    Examples
    --------
    ****
    '''
    for i, coord in  enumerate(coord_subcubes):
        xlo, ylo, xhi, yhi = coord
        plt.plot([xlo, xhi, xhi, xlo, xlo],
                 [ylo, ylo, yhi, yhi, ylo],
                 color=color, ls=l_s, lw=l_w)
        plt.annotate(f'{i}',
                     xy=(np.mean([xlo, xhi]),
                         np.mean([ylo, yhi]))
                     )

def plot_border(wcs, n_pix):
    '''Plot boundaries of subcubes
    Parameters
    ----------
    wcs: object
        ****
    n_pix: int
        Number of pixels of the cube side.
    Returns
    -------
    ****
    Examples
    --------
    ****
    '''
    brc = wcs.pixel_to_world(0,0,0)[0]
    trc = wcs.pixel_to_world(0,n_pix,0)[0]
    tlc = wcs.pixel_to_world(n_pix,n_pix,0)[0]
    blc = wcs.pixel_to_world(n_pix,0,0)[0]
    plt.plot([brc.ra.deg, trc.ra.deg, tlc.ra.deg, blc.ra.deg, brc.ra.deg],
             [brc.dec.deg, trc.dec.deg, tlc.dec.deg, blc.dec.deg, brc.dec.deg],
            'k-', lw=4)



def write_subcubes(steps, wcs, overlap, subcube_size_pix):
    '''Return coordinates of subcubes. Save file coord_subcubes.csv in the results
    folder containing the coordinates of the subcubes
    Parameters
    ----------
    steps: int
        Steps to grid the cube.
    wcs: object
        ****
    overlap: int
        Number of pixels overlaping between subcubes ****
    subcube_size_pix: int
        ****
    Returns
    -------
    coord_subcubes=array
        Array containing coordinates of subcubes.
    Examples
    --------
    ****
    '''
    ## Find subcubes coordinates and write them
    coord_subcubes = define_subcubes(steps, wcs, overlap, subcube_size_pix)
    np.savetxt("results/coord_subcubes.csv", coord_subcubes, delimiter=",",
               header="xlo,ylo,xhi,yhi",
               fmt="%f", comments='')
    return coord_subcubes

def plot_grid(wcs, coord_subcubes, grid_plot, n_pix):
    ''' Plot grid of subcubes
    Parameters
    ----------
    wcs: object
        ****
    coord_subcubes: array
        Array containing coordinates of subcubes.
    grid_plot: ****
        ****
    n_pix: int
        Number of pixels of the side of the cube.
    Returns
    -------
    ****
    Examples
    --------
    ****
    '''
    # It is not correcly projecting the pixels when using this mode.
    #Alternatively, I could use APLpy
    #plt.subplot(projection=wcs, slices=['x','y', 0])
    plt.subplot()
    plot_border(wcs, n_pix)
    plot_subcubes(coord_subcubes)
    #plt.grid()
    plt.xlabel('R.A. [deg]')
    plt.ylabel('Dec. [deg]')
    plt.gca().invert_xaxis()
    plt.savefig(grid_plot, bbox_inches='tight', dpi=200)

def main():
    '''Chunk the data cube in several subcubes'''
    args = get_args()
    infile = args.datacube
    grid_plot = args.grid_plot
    num_subcubes = int(args.num_subcubes)
    pixel_overlap = int(args.pixel_overlap)

    # Read the cube and coordinates definition
    cube = SpectralCube.read(infile)
    wcs = cube.wcs
    n_pix = wcs.array_shape[1]

    # Define subcube properties
    subcube_size_pix = int(n_pix/np.sqrt(num_subcubes))
    steps = np.arange(0, n_pix+1, subcube_size_pix)[:-1]
    overlap = pixel_overlap
    print(f"n_pix = {n_pix}")
    print(f"overlap = {overlap}")
    print(f"subcube_size_pix = {subcube_size_pix}")
    print(f"Number of subcubes = {num_subcubes}")
    print(f"steps = {steps}")

    coord_subcubes = write_subcubes(steps, wcs, overlap, subcube_size_pix)
    plot_grid(wcs, coord_subcubes, grid_plot, n_pix)

if __name__ == '__main__':
    main()
