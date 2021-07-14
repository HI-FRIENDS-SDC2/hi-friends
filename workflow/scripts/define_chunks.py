import sys
from spectral_cube import SpectralCube
import numpy as np
import matplotlib.pyplot as plt

#infile = '/mnt/scratch/jmoldon/processing/SDC2/data/development_large/cont_ldev.fits'
#infile = '/mnt/scratch/jmoldon/processing/SDC2/data/development_large/sky_ldev_v2.fits'

#infile = '/mnt/scratch/sdc2/data/development_large/cont_ldev.fits'
#infile = '/mnt/scratch/sdc2/data/development_large/sky_ldev_v2.fits'

#infile = '/mnt/sdc2-datacube/sky_full_v2.fits'
#infile = '/mnt/scratch/sdc2/data/development_large/sky_ldev_v2.fits'

infile = sys.argv[-1]

cube = SpectralCube.read(infile)
wcs = cube.wcs
N = wcs.array_shape[1]

def plot_border(wcs, N):
    brc = wcs.pixel_to_world(0,0,0)[0]
    trc = wcs.pixel_to_world(0,N,0)[0]
    tlc = wcs.pixel_to_world(N,N,0)[0]
    blc = wcs.pixel_to_world(N,0,0)[0]
    plt.plot([brc.ra.deg, trc.ra.deg, tlc.ra.deg, blc.ra.deg, brc.ra.deg],
             [brc.dec.deg, trc.dec.deg, tlc.dec.deg, blc.dec.deg, brc.dec.deg],
            'k-', lw=4)

subcube_size_pix = int(N/9)
steps = np.arange(0, N, subcube_size_pix)[:-1]
overlap = 40
print(f"N = {N}")
print(f"overlap = {overlap}")
print(f"subcube_size_pix = {subcube_size_pix}")
print(f"steps = {steps}")


def define_subcubes(steps, wcs, overlap):
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
## Find subcubes coordinates and write them
coord_subcubes = define_subcubes(steps, wcs, overlap)
np.savetxt("resources/coord_subcubes.csv", coord_subcubes, delimiter=",",
           header="xlo,ylo,xhi,yhi", 
           fmt="%f", comments='')

#c = coord_subcubes[15]
#sub_cube = cube.subcube(xlo=c[0], xhi=c[2], 
#                        ylo=c[1], yhi=c[3])

## Plot grid of subcubes

#plt.subplot(projection=wcs, slices=['x','y', 0])  # It is not correcly projecting the pixels when using this mode. Alternatively, I could use APLpy
plt.subplot()
plot_border(wcs, N)
plot_subcubes(coord_subcubes)
#plt.grid()
plt.xlabel('R.A. [deg]')
plt.ylabel('Dec. [deg]')
plt.gca().invert_xaxis()

plt.savefig('resources/grid.png', bbox_inches='tight', dpi=200)        

## Only the grid of pixels
#for sx in steps:
#    for sy in steps:
#        print(sx, sx+s, sy, sy+s)
#        plt.plot([sx-overlap/2, sx+s+overlap/2, sx+s+overlap/2, sx-overlap/2, sx-overlap/2],
#                  [sy-overlap/2, sy-overlap/2, sy+s+overlap/2, sy+s+overlap/2, sy-overlap/2], '-')
