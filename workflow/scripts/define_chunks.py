import sys
import argparse
from spectral_cube import SpectralCube
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Define coordinates of grid of subcubes'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--datacube', dest='datacube', help='Data cube to process.')
    parser.add_argument('-g', '--gridplot', dest='grid_plot', help='NAme of output file to plot the grid of subcubes')
    parser.add_argument('-n', '--num_subcubes', dest='num_subcubes', help='Total number of subcubes to divide the master cube')
    parser.add_argument('-o', '--overlap', dest='pixel_overlap', help='Number of pixels to extend the cube in each direction.')
    args = parser.parse_args()
    return args

def define_subcubes(steps, wcs, overlap, subcube_size_pix):
    coord_subcubes = []
    for sx in steps:
        for sy in steps:
            c0 = wcs.pixel_to_world(sx-overlap/2, sy-overlap/2, 0)[0]
            c1 = wcs.pixel_to_world(sx+subcube_size_pix+overlap/2, sy+subcube_size_pix+overlap/2, 0)[0]
            xlo = c0.ra.deg
            xhi = c1.ra.deg
            ylo = c0.dec.deg
            yhi = c1.dec.deg
            coord_subcubes.append([xlo,ylo, xhi, yhi])
            #print(sx-overlap/2, sy-overlap/2, sx+subcube_size_pix+overlap/2, sy+subcube_size_pix+overlap/2)
            #print(xlo, xhi, ylo, yhi)
    return np.array(coord_subcubes)

def plot_subcubes(coord_subcubes, ls='-', color=None, lw=1):
    for i, coord in  enumerate(coord_subcubes):
        xlo, ylo, xhi, yhi = coord
        plt.plot([xlo, xhi, xhi, xlo, xlo],
                 [ylo, ylo, yhi, yhi, ylo],
                 color=color, ls=ls, lw=lw)
        plt.annotate(f'{i}',
                     xy=(np.mean([xlo, xhi]),
                         np.mean([ylo, yhi]))
                     )

def plot_border(wcs, N):
    brc = wcs.pixel_to_world(0,0,0)[0]
    trc = wcs.pixel_to_world(0,N,0)[0]
    tlc = wcs.pixel_to_world(N,N,0)[0]
    blc = wcs.pixel_to_world(N,0,0)[0]
    plt.plot([brc.ra.deg, trc.ra.deg, tlc.ra.deg, blc.ra.deg, brc.ra.deg],
             [brc.dec.deg, trc.dec.deg, tlc.dec.deg, blc.dec.deg, brc.dec.deg],
            'k-', lw=4)



def write_subcubes(steps, wcs, overlap, subcube_size_pix):
    ## Find subcubes coordinates and write them
    coord_subcubes = define_subcubes(steps, wcs, overlap, subcube_size_pix)
    np.savetxt("results/coord_subcubes.csv", coord_subcubes, delimiter=",",
               header="xlo,ylo,xhi,yhi", 
               fmt="%f", comments='')
    return coord_subcubes

def plot_grid(wcs, coord_subcubes, grid_plot, N):
    ## Plot grid of subcubes
    #plt.subplot(projection=wcs, slices=['x','y', 0])  # It is not correcly projecting the pixels when using this mode. Alternatively, I could use APLpy
    plt.subplot()
    plot_border(wcs, N)
    plot_subcubes(coord_subcubes)
    #plt.grid()
    plt.xlabel('R.A. [deg]')
    plt.ylabel('Dec. [deg]')
    plt.gca().invert_xaxis()
    plt.savefig(grid_plot, bbox_inches='tight', dpi=200)        

def main():
    args = get_args()
    infile = args.datacube
    grid_plot = args.grid_plot
    num_subcubes = int(args.num_subcubes)
    pixel_overlap = int(args.pixel_overlap)

    # Read the cube and coordinates definition 
    cube = SpectralCube.read(infile)
    wcs = cube.wcs
    N = wcs.array_shape[1]
    
    # Define subcube properties
    subcube_size_pix = int(N/np.sqrt(num_subcubes))
    steps = np.arange(0, N, subcube_size_pix)#[:-1]
    overlap = pixel_overlap
    print(f"N = {N}")
    print(f"overlap = {overlap}")
    print(f"subcube_size_pix = {subcube_size_pix}")
    print(f"Number of subcubes = {num_subcubes}")
    print(f"steps = {steps}")

    coord_subcubes = write_subcubes(steps, wcs, overlap, subcube_size_pix)
    plot_grid(wcs, coord_subcubes, grid_plot, N)

if __name__ == '__main__':
    main()


