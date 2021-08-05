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
from astropy import constants as const
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
import pandas as pd

def get_args():
    '''This function parses and returns arguments passed in'''
    description = 'Eliminate duplicates from catalog for sources in the overlapping regions'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--infile', dest='infile', \
                        help='catalog without duplicated sources')
    parser.add_argument('-o', '--outfile', dest='outfile',\
                        help='filtered catalog')
    args = parser.parse_args()
    return args

def arcsec2kpc(redshift, theta):
    '''Converts angular size to linear size given a redshift

    Parameters
    ----------
    redshift: float
        redshift
    theta: array of floats
        angular size in arcsec
    Returns
    -------
    distance_kpc: array of floats
        linear size in kpc
    '''
    cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    d_a = cosmo.angular_diameter_distance(z=redshift)
    distance_kpc = (theta*u.arcsec * d_a).to(u.kpc, u.dimensionless_angles())
    return distance_kpc

def compute_d_m(cat):
    '''Computes the Mass of HI and linear diameter of the galaxies in a catalog

    Parameters
    ----------
    cat: pandas.DataFrame
        catalog of galaxies
    Returns
    -------
    cat: pandas.DataFrame
        original catalog adding the columns log(M_HI) and log(D_HI_kpc)
    '''
    cspeed = const.c.value/1000      # km/s
    h_small = 0.7
    f0_hi = 1420405751.786
    size = cat['hi_size'] # arcsec
    redshift = (f0_hi-cat['central_freq'])/cat['central_freq']
    distance_kpc = arcsec2kpc(redshift.values, size.values)

    # Equation (37) of https://arxiv.org/pdf/1705.04210.pdf
    flux_jy_km_s = cat['line_flux_integral']*(cspeed*(1+redshift)**2)/f0_hi
    vel = (cat['central_freq'].values * u.Hz).to(u.km / u.s,
           equivalencies=freq_to_vel())
    distance_mpc = vel/70
    m_hi_units = (1/h_small**2)*235600*flux_jy_km_s*(distance_mpc*h_small)**2
    d_hi_kpc = np.array(distance_kpc)
    m_hi = np.array(m_hi_units)
    cat['logM'] = np.log10(m_hi)
    cat['logD'] = np.log10(d_hi_kpc)
    return cat

def filter_md(df_md, uplim=0.45, downlim=-0.15):
    ''' Removes items from a catalog based on distance from the
    Wang et al. 2016 2016MNRAS.460.2143W correlation. The values used
    are log DHI= (0.506±0.003) log MHI−(3.293±0.009)

    Parameters
    ----------
    df_md: pandas DataFrame
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
    cond1 = (df_md['logD'] - (0.506 * df_md['logM'] -3.293)) < downlim
    cond2 = (df_md['logD'] - (0.506 * df_md['logM'] -3.293)) > uplim
    cond=cond1 | cond2
    df_out = df_md[~cond]
    return df_out

def freq_to_vel(f0_hi=1420405751.786):
    '''Convers line frequency to velocity in km/s

    Parameters
    ----------
    f0_hi: float
        rest frequency of the spectral line
    Returns
    -------
    freq2vel: function
        function to convert frequency in Hz to velocity
    '''
    restfreq = f0_hi * u.Hz
    freq2vel = u.doppler_radio(restfreq)
    return freq2vel

def main():
    '''Gets an input catalog and filters the sources based on deviation
    from the D_HI M_HI correlation'''
    args = get_args()
    dataf = pd.read_csv(args.infile, delimiter=' ')
    dataf_md = compute_d_m(dataf)
    dataf_md_file = (args.infile).replace('.csv', '_logMD.csv')
    dataf_md.to_csv(dataf_md_file, sep=' ', index=False)
    # Filter based of correlation
    dataf_filtered = filter_md(dataf_md)
    dataf_filtered.to_csv(dataf_md_file.replace('.csv', '_filtered.csv'),
        sep=' ', index=False)
    dataf_filtered = dataf_filtered.drop(columns=['logM', 'logD'])
    print(f'Number of entried before filtering: {len(dataf_md)}')
    print(f'Number of entried after  filtering: {len(dataf_filtered)}')
    dataf_filtered.to_csv(args.outfile, sep=' ', index=False)


if __name__ == '__main__':
    main()
