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
This script converts sofia Catalog to the SDC2 catalog
'''


import os
import argparse
import re
import pandas as pd
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy import constants as const

cspeed = const.c.value      # m/s
F0_H1 = 1420405751.786    # Hz

def get_args():
    '''This function parses and returns arguments passed in'''
    description = 'Select dataset'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--results_path', dest='results_path', \
                        help='Directory for results', default='results')
    parser.add_argument('-o', '--outname', dest='outname', help='Name of \
                        output directory for Sofia products', default='test')
    parser.add_argument('-d', '--datacube', dest='datacube', help='Data cube \
                        to process. Options are: development, development_large,\
                        evaluation', default='development')
    parser.add_argument('-i', '--incatalog', dest='incatalog', help='Path of \
                        the input Sofia catalog to be converted', \
                        default='development')
    args = parser.parse_args()
    return args

def read_sofia_header(filename):
    '''Reads SOFIA header
    Parameters
    ----------
    filename: str
        Input file name
    Returns
    -------
    head: str
        Header of input file
    '''
    with open(filename, 'r') as infile:
        head_line = infile.readlines()[10]
    head = re.split('\s+', head_line.strip('\n'))[1:] # 1: to remove #
    return head

def sofia2cat(catalog):
    '''Runs sofia and returns the raw catalog filtered with galaxies that have
       kinematic position angle greater than zero
    Parameters
    ----------
    catalog: str
        Input file name
    Returns
    -------
    raw_cat_filtered: pandas DataFrame
        Raw catalog produced by sofia filtered by kinematic position angle
        greater than zero.
    '''
    head = read_sofia_header(catalog)
    raw_cat = pd.read_csv(catalog, delim_whitespace=True, header=None, \
                          names=head, comment='#')
    raw_cat.sort_values(by='f_sum', ascending=False, inplace=True)
    raw_cat_filtered = raw_cat[raw_cat['kin_pa']>0]
    print('Producing sofia raw catalog filtered by kin_pa > 0:')
    return raw_cat_filtered

def pix2coord(wcs, pix_x, pix_y):
    '''
    Converts pixels to coordinates using WCS header info
    Parameters
    ----------
    wcs: class astropy.wcs
        wcs of the fits file
    pix_x: int
        Pixel number in X direction
    pix_y: int
        Pixel number in Y direction
    Returns
    -------
    coord[0].ra.deg: float
        Right ascension in degrees
    coord[0].dec.deg: float
        Declination in degrees
    '''
    coord = wcs.pixel_to_world(pix_x, pix_y, 1)
    return coord[0].ra.deg, coord[0].dec.deg

def compute_inclination(bmaj, bmin):
    '''Computes inclinaton
    See A7) in http://articles.adsabs.harvard.edu/pdf/1992MNRAS.258..334S
    Note p has been implemented as varp and q has been implemented as vaarq
    Parameters
    ----------
    bmaj: float
        Major axis of ellipse fitted to the galaxy in arcsec
    pix_x: float
        Minor axis of ellipse fitted to the galaxy in arcsec
    Returns
    -------
    np.degrees(np.arccos(cosi)): float
        Inclination in degrees
    '''
    varp = bmin/bmaj
    varq = 0.65*varp - 0.072*varp**3.9
    cosi = np.sqrt(
            (varp**2 - varq**2)/(1-varq**2)
            )
    cosi[np.isnan(cosi)] = 0.0
    return np.degrees(np.arccos(cosi))

def convert_units(raw_cat, fitsfile):
    '''Convert units from raw catalog into fitsfile
    Parameters
    ----------
    raw_cat: pandas DataFrame
        Raw catalog
    fitsfile: string
        Path to fits file
    Returns
    -------
    ra_deg: array of floats
        Right ascension
    dec_deg: array of floats
        Declination
    pix2arcsec: float
        Conversion factor from pixel units to arcsec
    pix2freq: float
        Conversion factor from channel to Hz
    '''

    file = fits.open(fitsfile)
    wcs=WCS(file[0].header)
    file.close()
    # Convert x,y in pixels to R.A.,Dec. in deg
    ra_deg, dec_deg = pix2coord(wcs, raw_cat['x'], raw_cat['y'])
    # Get pixel size
    pix2arcsec = wcs.wcs.get_cdelt()[1]*3600. # This assumes same pixel size
                                              #in both direction
    pix2freq = file[0].header['CDELT3']
    return ra_deg, dec_deg, pix2arcsec,pix2freq

def frequency_to_vel(freq, invert=False):
    '''Convert frequency to velocity
    Parameters
    ----------
    freq: float
        Frequency in Hz
    invert: boolean
        If invert is false then returns velocity.
        If invert is true returns frequency.
    Returns
    -------
    ra_deg: array of floats
        Right ascension
    dec_deg: array of floats
        Declination
    pix2arcsec: float
        Conversion factor from pixel units to arcsec
    pix2freq: float
        Conversion factor from channel to Hz
    '''
    if not invert:
        return cspeed*((F0_H1**2-freq**2)/(F0_H1**2+freq**2))
    else:
        return F0_H1*np.sqrt((1-freq/cspeed)/(1+freq/cspeed))

def convert_flux(flux,filename):
    '''This assume that flux comes from SoFiA in Jy/beam and converts it
    to Jy * km/s base on the header
    Parameters
    ----------
    flux: array of floats
        Flux in Jy/beam
    filename: str
        Name of input file
    Returns
    -------
    flux/pix_per_beam*cdelt_hz: array of floats
        flux in Jy*Hz
    '''

    hdr = fits.getheader(filename)
    print(hdr['BMAJ'],hdr['BMIN'])
    beamarea=(np.pi*abs(hdr['BMAJ']*hdr['BMIN']))/(4.*np.log(2.))
    pix_per_beam = beamarea/(abs(hdr['CDELT1'])*abs(hdr['CDELT2']))
    cdelt_hz = float(hdr['CDELT3'])
    return flux/pix_per_beam*cdelt_hz    #Jy * hz

def convert_frequency_axis(filename, outname, velocity_req = 'radio'):
    '''Convert the frequency axis of a cube
    Parameters
    ----------
    filename: str
        Name of input file
    outname: str
        Name of output file
    velocity_req: str
        velocity definition framework
    '''
    c_ms = cspeed*1000.
    print(filename)
    cube = fits.open(filename)
    hdr = cube[0].header
    # Check we have a proper third axis
    if hdr['CTYPE3'].lower() != 'freq' or hdr['NAXIS'] < 3:
        print('We can not convert this axis as it is not a frequency axis')
        return

    # get central values
    crpix = float(hdr['CRPIX3'])
    crval = float(hdr['CRVAL3'])
    naxis_len = float(hdr['NAXIS3'])
    # make sure the central pixel is rather central else large errors
    # are introduce in both vrad and rel. Check previuos versios of the code
    # if naxis_len/2.-5 < crpix <  naxis_len/2.+5:
    #     hdr_wcs = WCS(hdr)
    #     centralx,centraly, new_freq = hdr_wcs.pix2world([hdr['CRPIX1'], \
    #                                          hdr['CRPIX2'],naxis_len/2.],1)
    #     # Might need this hdr['CRPIX3'] = new_pix
    #     crval = new_freq
    #Now convert
    if velocity_req == 'radio':
      # convert from frequency to radio velocity
        cdelt_vel = -c_ms*float(hdr['CDELT3'])/F0_H1
        crval_vel = c_ms*(1-crval/F0_H1)
      # https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf
        hdr['CTYPE3'] = 'VRAD'
    elif velocity_req == 'relativistic':
        # This should always only ever be used for cubes with small velocity range
        crval_vel = frequency_to_vel(crval)
        freqstep = float(hdr['CDELT3'])
        central_two = frequency_to_vel(crval+freqstep)
        lower_one = frequency_to_vel(crval-(naxis_len/2.)*freqstep)
        lower_two = frequency_to_vel(crval-(naxis_len/2.+1)*freqstep)
        upper_one = frequency_to_vel(crval+(naxis_len/2.-1.)*freqstep)
        upper_two = frequency_to_vel(crval+(naxis_len/2.)*freqstep)
        cdelt_vel = np.mean([central_two-crval_vel,lower_two-lower_one,upper_two-upper_one])*1000.
        if cdelt_vel*naxis_len > 1e6:
            print('This cube is too big for a relativistic conversion')
            return
        hdr['CTYPE3'] = 'VELO'
    else:
        print('We dont do those things here.')
        return
    hdr['CDELT3'] = cdelt_vel
    hdr['CRVAL3'] = crval_vel

    if 'CUNIT3' in hdr:
        # delete cunit3 because we adopt the default units = m/s
        del hdr['CUNIT3']
    fits.writeto(outname,cube[0].data,hdr,overwrite = True)

def process_catalog(raw_cat, fitsfile):
    '''Process catalog
    Parameters
    ----------
    raw_cat: pandas.DataFrame
        Raw catalog
    fitsfile: str
        Path to fits file of processed data cube 
    Returns
    -------
    processed_cat: pandas.DataFrame
        Processed catalog
    '''
    # Unit conversion
    ra_deg, dec_deg, pix2arcsec,pix2freq = convert_units(raw_cat, fitsfile)
    hi_size = raw_cat['ell_maj']*pix2arcsec
    # Estimate inclination based on fitted ellipsoid, assuming the galaxy is
    # intrinsically circular
    inclination = compute_inclination(raw_cat['ell_maj'], raw_cat['ell_min'])

    # Construct the output catalog
    processed_cat = pd.DataFrame()
    processed_cat['id_subcube'] = raw_cat['id']
    processed_cat['ra'] = ra_deg
    processed_cat['dec'] = dec_deg
    processed_cat['hi_size'] = hi_size
    # Now converted to Jy*km/s verifcation for developments needed
    processed_cat['line_flux_integral'] = convert_flux(raw_cat['f_sum'],\
                                                       fitsfile)
    if 'freq' in raw_cat:
        processed_cat['central_freq'] =  raw_cat['freq']
        processed_cat['w20'] = frequency_to_vel(raw_cat['freq']-\
                               raw_cat['w20']/2.*pix2freq)-\
                               frequency_to_vel(raw_cat['freq']+\
                               raw_cat['w20']/2.*pix2freq) # we need to clarify
                                   # if the units and the definition is the same
    else:
        #processed_cat['central_velocity'] =  raw_cat['v_app']
        if 'v_app' in raw_cat.columns:
            print('Using v_app column')
            processed_cat['central_freq'] = frequency_to_vel(raw_cat['v_app'],\
                                                             invert=True)
        elif 'freq' in raw_cat.columns:
            print('Using freq column')
            processed_cat['central_freq'] = raw_cat['freq']
        # This case should not be included for production,
        # just to test the minimal cube
        elif 'v_opt' in raw_cat.columns:
            print('WARNING. Using v_opt column. Use only to check the workflow')
            processed_cat['central_freq'] = frequency_to_vel(raw_cat['v_opt'],\
                                                             invert=True)
        processed_cat['w20'] = raw_cat['w20']*pix2freq
         # we need to clarify if what sofia gives is the central freq
    processed_cat['w20'] *= 1e-3 # To convert from m/s to km/s
    # we need to clarify if Sofia kinematic angle agrees with their P.A.
    processed_cat['pa'] = raw_cat['kin_pa']
    processed_cat['i'] = inclination
    processed_cat['rms'] = raw_cat['rms']
    processed_cat['subcube'] = os.path.basename(fitsfile).split('_')[1].split('.fits')[0]
    processed_cat.reset_index(drop=True, inplace=True)
    # This is just to set the right order of the output columns
    processed_cat = processed_cat[['id_subcube', 'ra', 'dec', 'hi_size', \
                                   'line_flux_integral', 'central_freq', 'pa', \
                                   'i', 'w20', 'rms', 'subcube']]
    processed_cat['central_freq'] = processed_cat['central_freq'].map('{:.1f}'.format)
    return processed_cat

def find_fitsfile(parfile):
    """ Searchs in the parfile the name of the fits file used
    Parameters
    ----------
    parfile: str
        Parameters file
    Returns
    -------
    fitsfile: str
        Path to fits file of processed data cube
    """
    with open(parfile, 'r') as infile:
        for line in infile.readlines():
            if 'input.data' in line:
                break
        fitsfile = line.split('=')[1].strip()
    return fitsfile


def main():
    ''' Converts sofia Catalog to the SDC2 catalog'''
    args = get_args()
    output_path = os.path.join(args.results_path, args.outname)
    incatalog = args.incatalog
    raw_cat = sofia2cat(catalog=incatalog)
    fitsfile = find_fitsfile(os.path.join(output_path, 'sofia.par'))
    processed_cat = process_catalog(raw_cat, fitsfile)
    final_cat_file = incatalog.replace('_cat.txt', '_final_catalog.csv')
    processed_cat.to_csv(final_cat_file, sep=' ', index=False)

if __name__ == '__main__':
    main()
