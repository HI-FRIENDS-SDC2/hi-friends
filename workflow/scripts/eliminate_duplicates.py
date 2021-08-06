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
This script removes duplicates and creates a catalog without duplicated sources
'''

import argparse
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table

def get_args():
    '''This function parses and returns arguments passed in'''
    description = 'Eliminate duplicates from catalog for sources in the overlapping regions'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--infile', dest='infile', \
                        help='catalog with duplicated sources')
    parser.add_argument('-o', '--outfile', dest='outfile',\
                        help='catalog without duplicated sources')
    args = parser.parse_args()
    return args

def read_ref_catalog(infile, name_list):
    '''Reads the catalog with the variables from an input string


    Parameters
    ----------
    infile: str
        Input file name
    name_list: str
        List of varible names
    Returns
    -------
    catalog_table: astropy.Table
        table with the data
    '''
    catalog_table = Table.read(infile, format='ascii', delimiter=' ', \
                               names=name_list)
    return catalog_table

def read_coordinates_from_table(cat):
    '''Reads coordinates from a table

    Parameters
    ----------
    cat: astropy.Table
        table with coordinates
    Returns
    -------
    ras: float
        Right ascension
    dec: float
        Declination
    freq: float
        Frequency
    '''
    ras = cat['ra']*u.degree
    dec = cat['dec']*u.degree
    freq = cat['central_freq']*u.Hz
    return ras, dec, freq

def find_catalog_duplicates(ras, dec, freq):
    '''Finds duplicates in the catalog

    Parameters
    ----------
    ras: float
        Right ascension
    dec: float
        Declination
    freq: float
        Frequency
    Returns
    -------
    cond: Bool array
        array storing proximity criteria
    idx: int array
         Index of the duplicated sources
    '''
    coord = SkyCoord(ra=ras, dec=dec)
    idx, d2d, _ = coord.match_to_catalog_sky(coord, nthneighbor=2)
    max_sep = 3 * u.arcsec
    sep_constraint = d2d < max_sep
    max_freq = 20 * u.MHz
    freq_sep = abs(freq - freq[idx])
    freq_constraint = freq_sep < max_freq
    cond = sep_constraint * freq_constraint
    return cond, idx

def mask_worse_duplicates(cond, idx, catalog_table):
    '''Finds worse duplicates and masks them

    Parameters
    ----------
    cond: Bool array
        array storing proximity criteria
    idx: int array
         Index of the duplicated sources
    catalog_table: astropy.Table
        table with detections
    Returns
    -------
    duplicates: Bool array
        array with True when source is duplicated
    '''
    duplicates = np.copy(cond)
    print('id1 subcube1 id_subcube1 rms1 id2 subcube2 id_subcube2 rms2')
    # Here we are counting all matches twice.
    # We could directly use the first half of the matches
    for i in np.where(cond)[0]:
        id1 = catalog_table[idx[i]]['id_subcube']
        id2 = catalog_table[i]['id_subcube']
        rms1 = catalog_table[idx[i]]['rms']
        rms2 = catalog_table[i]['rms']
        subcube1 = catalog_table[idx[i]]['subcube']
        subcube2 = catalog_table[i]['subcube']
        print(f"{idx[i]:2d} {subcube1} {id1} {rms1} {i} {subcube2} {id2} {rms2}")
        if catalog_table[idx[i]]['rms'] < catalog_table[i]['rms']:
            duplicates[idx[i]] = False
        else:
            duplicates[i] = False
    print(f'Total number of duplicated sources: {int(len(np.where(cond)[0])/2)}')
    return duplicates


def main():
    '''Removes duplicates and creates a catalog without duplicated sources'''
    args = get_args()
    name_list = ['id_subcube', 'ra', 'dec', 'hi_size', 'line_flux_integral', \
                 'central_freq', 'pa', 'i', 'w20', 'rms', 'subcube']
    catalog_table = read_ref_catalog(args.infile, name_list=name_list)
    ras, dec, freq = read_coordinates_from_table(catalog_table)
    cond, idx = find_catalog_duplicates(ras, dec, freq)
    duplicates = mask_worse_duplicates(cond, idx, catalog_table)
    final_table = catalog_table[~duplicates][name_list[:-1]]
    final_table.sort(['ra', 'dec'])
    final_table['id'] = range(len(final_table))
    name_list_out = ['id', 'ra', 'dec', 'hi_size', 'line_flux_integral', \
                     'central_freq', 'pa', 'i', 'w20']
    final_table = final_table[name_list_out]
    final_table.write(args.outfile, names=name_list_out, format='ascii', \
                      overwrite=True)


if __name__ == '__main__':
    main()
