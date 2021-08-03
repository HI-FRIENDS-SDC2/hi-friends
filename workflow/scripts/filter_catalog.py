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
This script filters the output catalog based on some conditions
'''

import argparse
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy import constants as const
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import pandas as pd

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Eliminate duplicates from catalog for sources in the overlapping regions'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--infile', dest='infile', \
                        help='catalog without duplicated sources')
    parser.add_argument('-o', '--outfile', dest='outfile',\
                        help='filtered catalog')
    args = parser.parse_args()
    return args

def arcsec2kpc(z, theta):
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    d_A = cosmo.angular_diameter_distance(z=z)
    distance_kpc = (theta*u.arcsec * d_A).to(u.kpc, u.dimensionless_angles())
    return distance_kpc

def compute_D_M(cat):
    cspeed = const.c.value/1000      # km/s
    h_small = 0.7
    f0_HI = 1420405751.786
    size = cat['hi_size'] # arcsec
    z = (f0_HI-cat['central_freq'])/cat['central_freq']
    distance_kpc = arcsec2kpc(z.values, size.values)

    # Equation (37) of https://arxiv.org/pdf/1705.04210.pdf
    flux_Jy_km_s = cat['line_flux_integral']*(cspeed*(1+z)**2)/f0_HI 
    vel = (cat['central_freq'].values * u.Hz).to(u.km / u.s,
           equivalencies=freq_to_vel()) 
    distance_Mpc = vel/70
    M_HI_units = (1/h_small**2)*235600*flux_Jy_km_s*(distance_Mpc*h_small)**2
    D_HI_kpc = np.array(distance_kpc)
    M_HI = np.array(M_HI_units)
    cat['logM'] = np.log10(M_HI)
    cat['logD'] = np.log10(D_HI_kpc)
    return cat

def filter_MD(df_MD, uplim=0.45, downlim=-0.15):
    ''' Removes items from a catalog based on distance from the 
    Wang et al. 2016 2016MNRAS.460.2143W correlation. The values used
    are log DHI= (0.506±0.003) log MHI−(3.293±0.009)

    Parameters
    ----------
    df_MD: pandas DataFrame
        input catalog in pandas format
    uplim: float
        Threshold distance to consider outliers in the top region
    downlim: float
        Threshold distance to consider outliers in the bottom region
    Returns
    -------
    df_out: pandas DataFrame
        output catalog without the outliers
    '''
    cond1 = (df_MD['logD'] - (0.506 * df_MD['logM'] -3.293)) < downlim
    cond2 = (df_MD['logD'] - (0.506 * df_MD['logM'] -3.293)) > uplim
    cond=cond1 | cond2
    df_out = df_MD[~cond]
    return df_out

def freq_to_vel(f0=1420405751.786):
    restfreq = f0 * u.Hz  # rest frequency of 12 CO 1-0 in GHz
    freq2vel = u.doppler_radio(restfreq)
    return freq2vel

def main():
    '''Gets an input catalog and filters the sources based on deviation
    from the D_HI M_HI correlation'''
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    args = get_args()
    df = pd.read_csv(args.infile, delimiter=' ')
    df_MD = compute_D_M(df)
    df_MD_file = (args.infile).replace('.csv', '_logMD.csv')
    df_MD.to_csv(df_MD_file, sep=' ', index=False)
    # Filter based of correlation
    df_filtered = filter_MD(df_MD)
    dffiltered = df_filtered.drop(columns=['logM', 'logD'])
    print(f'Number of entried before filtering: {len(df_MD)}')
    print(f'Number of entried after  filtering: {len(df_filtered)}')
    df_filtered.to_csv(args.outfile, sep=' ', index=False)


if __name__ == '__main__':
    main()

