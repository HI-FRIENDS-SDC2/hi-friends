import sys
import numpy as np
from spectral_cube import SpectralCube
from astropy import units as u

idx = int(sys.argv[-1])
infile = '/mnt/scratch/jmoldon/processing/SDC2/data/development/sky_dev_v2.fits'

coord_subcubes = np.loadtxt('resources/coord_subcubes.csv', skiprows=1, delimiter=',')
#print(coord_subcubes)

print(f'Now exporting item {idx}')
print(coord_subcubes[idx])
c = coord_subcubes[idx]

cube = SpectralCube.read(infile)
sub_cube = cube.subcube(xlo=c[0]*u.deg, xhi=c[2]*u.deg,
                        ylo=c[1]*u.deg, yhi=c[3]*u.deg)

#sub_cube.write(f'resources/subcubes/subcube_{idx:02d}.fits')
sub_cube.write(f'resources/subcubes/subcube_{idx}.fits')

