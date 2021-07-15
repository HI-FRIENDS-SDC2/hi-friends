import argparse
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import match_coordinates_sky
from astropy.table import Table
from astropy.io import fits

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Eliminate duplicates from catalog for sources in the overlapping regions'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--infile', dest='infile', help='catalog with duplicated sources')
    parser.add_argument('-o', '--outfile', dest='outfile', help='catalog without duplicated sources')
    args = parser.parse_args()
    return args

def read_ref_catalog(infile, name_list):
    catalog_table = Table.read(infile, format='ascii', delimiter=' ', names=name_list)
    return catalog_table

def read_coordinates_from_table(cat):
    ra = cat['ra']*u.degree
    de = cat['dec']*u.degree
    freq = cat['central_freq']*u.Hz
    return ra, de, freq

def find_catalog_duplicates(ra, de, freq):
    c = SkyCoord(ra=ra, dec=de)
    idx, d2d, d3d = c.match_to_catalog_sky(c, nthneighbor=2)
    max_sep = 3 * u.arcsec
    sep_constraint = d2d < max_sep
    max_freq = 20 * u.MHz
    freq_sep = abs(freq - freq[idx])
    freq_constraint = freq_sep < max_freq
    cond = sep_constraint * freq_constraint
    c_matches = c[cond]
    return cond, idx

def mask_worse_duplicates(cond, idx, catalog_table):
    duplicates = np.copy(cond)
    print(f'id1 subcube1 id_subcube1 rms1 id2 subcube2 id_subcube2 rms2')
    # Here we are counting all matches twice. We could directly use the first half of the matches
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
    args = get_args()
    name_list = ['id_subcube', 'ra', 'dec', 'hi_size', 'line_flux_integral', 'central_freq', 'pa', 'i', 'w20', 'rms', 'subcube']
    catalog_table = read_ref_catalog(args.infile, name_list=name_list)
    ra, de, freq = read_coordinates_from_table(catalog_table)
    cond, idx = find_catalog_duplicates(ra, de, freq)
    duplicates = mask_worse_duplicates(cond, idx, catalog_table)
    final_table = catalog_table[~duplicates][name_list[:-1]]
    final_table.sort(['ra', 'dec'])
    final_table['id'] = range(len(final_table))
    name_list_out = ['id', 'ra', 'dec', 'hi_size', 'line_flux_integral', 'central_freq', 'pa', 'i', 'w20']
    final_table = final_table[name_list_out]
    final_table.write(args.outfile, names=name_list_out, format='ascii', overwrite=True)


if __name__ == '__main__':
    main()

