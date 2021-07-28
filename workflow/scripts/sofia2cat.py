import os
import argparse
import subprocess
import pandas as pd
import numpy as np
import re
from astropy.io import fits
from astropy.wcs import WCS
from astropy import constants as const

c = const.c.value      # m/s
f0 = 1420405751.786    # Hz

def get_args():
    '''This function parses and returns arguments passed in'''
    # Assign description to the help doc
    description = 'Select dataset'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-r', '--results_path', dest='results_path', help='Directory for results', default='results')
    parser.add_argument('-o', '--outname', dest='outname', help='Name of output directory for Sofia products', default='test')
    parser.add_argument('-d', '--datacube', dest='datacube', help='Data cube to process. Options are: development, development_large, evaluation', default='development')
    parser.add_argument('-i', '--incatalog', dest='incatalog', help='Path of the input Sofia catalog to be converted', default='development')
    args = parser.parse_args()
    return args

def read_sofia_header(filename):
    with open(filename, 'r') as f:
        head_line = f.readlines()[10]
    head = re.split('\s+', head_line.strip('\n'))[1:] # 1: to remove #
    return head

def sofia2cat(catalog):
    head = read_sofia_header(catalog)
    raw_cat = pd.read_csv(catalog, delim_whitespace=True, header=None, names=head, comment='#')
    raw_cat.sort_values(by='f_sum', ascending=False, inplace=True)
    raw_cat_filtered = raw_cat[raw_cat['kin_pa']>0]
    print('Producing sofia raw catalog filtered by kin_pa > 0:')
    return raw_cat_filtered

def pix2coord(wcs, x, y):
    coord = wcs.pixel_to_world(x, y, 1)
    #print('coord')
    #print(coord)
    return coord[0].ra.deg, coord[0].dec.deg

def compute_inclination(bmaj, bmin, q=0.2):
    cosi = np.sqrt(((bmin/bmaj)**2 - q**2)/(1 - q**2))
    # From A7) in http://articles.adsabs.harvard.edu/pdf/1992MNRAS.258..334S 
    p = bmin/bmaj
    q = 0.65*p - 0.072*p**3.9
    cosi = np.sqrt(
            (p**2 - q**2)/(1-q**2)
            )
    cosi[np.isnan(cosi)] = 0.0
    return np.degrees(np.arccos(cosi))

def convert_units(raw_cat, fitsfile):
    f = fits.open(fitsfile)
    wcs=WCS(f[0].header)
    f.close()
    # Convert x,y in pixels to R.A.,Dec. in deg
    ra_deg, dec_deg = pix2coord(wcs, raw_cat['x'], raw_cat['y'])
    # Get pixel size
    pix2arcsec = wcs.wcs.get_cdelt()[1]*3600. # This assumes same pixel size in both direction
    pix2freq = f[0].header['CDELT3']
    return ra_deg, dec_deg, pix2arcsec,pix2freq

def frequency_to_vel(freq, invert=False):
    if not invert:
        return c*((f0**2-freq**2)/(f0**2+freq**2))
    else:
        return f0*np.sqrt((1-freq/c)/(1+freq/c))

def convert_flux(flux,filename):
    #This assume that flux comes from SoFiA in Jy/beam and converts it to Jy * km/s base on the header
    hdr = fits.getheader(filename)
    print(hdr['BMAJ'],hdr['BMIN'])
    beamarea=(np.pi*abs(hdr['BMAJ']*hdr['BMIN']))/(4.*np.log(2.))
    pix_per_beam = beamarea/(abs(hdr['CDELT1'])*abs(hdr['CDELT2']))
    #cdelt_vel = abs(-c*float(hdr['CDELT3'])/f0)
    cdelt_hz = float(hdr['CDELT3'])
    return flux/pix_per_beam*cdelt_hz    #Jy * hz

# Convert the frequency axis of a cube
def convert_frequency_axis(filename, outname, velocity_req = 'radio'):
    c_ms = c*1000.
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
    # make sure the central pixel is rather central else large errors are introduce in both vrad and rel
    if naxis_len/2.-5 < crpix <  naxis_len/2.+5:
            hdr_wcs = WCS(hdr)
            centralx,centraly, new_freq = hdr_wcs.pix2world([hdr['CRPIX1'],hdr['CRPIX2'],naxis_len/2.],1)
            hdr['CRPIX3'] = new_pix
            crval = new_freq
    #Now convert
    if velocity_req == 'radio':
          # convert from frequency to radio velocity
            cdelt_vel = -c_ms*float(hdr['CDELT3'])/f0
            crval_vel = c_ms*(1-crval/f0)
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
    # Unit conversion
    ra_deg, dec_deg, pix2arcsec,pix2freq = convert_units(raw_cat, fitsfile)
    hi_size = raw_cat['ell_maj']*pix2arcsec
    # Estimate inclination based on fitted ellipsoid, assuming the galaxy is intrinsically circular
    inclination = compute_inclination(raw_cat['ell_maj'], raw_cat['ell_min'])

    # Construct the output catalog
    processed_cat = pd.DataFrame()
    processed_cat['id_subcube'] = raw_cat['id']
    processed_cat['ra'] = ra_deg
    processed_cat['dec'] = dec_deg
    processed_cat['hi_size'] = hi_size
    processed_cat['line_flux_integral'] = convert_flux(raw_cat['f_sum'],fitsfile)  # Now converted to Jy*km/s verifcation for developments needed
    if 'freq' in raw_cat:
        processed_cat['central_freq'] =  raw_cat['freq']
        #processed_cat['central_velocity'] = frequency_to_vel(raw_cat['freq'])
        processed_cat['w20'] = frequency_to_vel(raw_cat['freq']-raw_cat['w20']/2.*pix2freq)-frequency_to_vel(raw_cat['freq']+raw_cat['w20']/2.*pix2freq) # we need to clarify if the units and the definition is the same
    else:
        #processed_cat['central_velocity'] =  raw_cat['v_app']
        if 'v_app' in raw_cat.columns:
            print('Using v_app column')
            processed_cat['central_freq'] = frequency_to_vel(raw_cat['v_app'],invert=True)
        elif 'freq' in raw_cat.columns:
            print('Using freq column')
            processed_cat['central_freq'] = raw_cat['freq']
        elif 'v_opt' in raw_cat.columns:  # This case should not be included for production, just to test the minimal cube
            print('WARNING. Using v_opt column. Use only to check the workflow')
            processed_cat['central_freq'] = frequency_to_vel(raw_cat['v_opt'],invert=True)
        processed_cat['w20'] = raw_cat['w20']*pix2freq
         # we need to clarify if what sofia gives is the central freq
    processed_cat['w20'] *= 1e-3 # To convert from m/s to km/s
    processed_cat['pa'] = raw_cat['kin_pa']  # we need to clarify if Sofia kinematic angle agrees with their P.A.
    processed_cat['i'] = inclination
    processed_cat['rms'] = raw_cat['rms']
    processed_cat['subcube'] = os.path.basename(fitsfile).split('_')[1].split('.fits')[0]
    processed_cat.reset_index(drop=True, inplace=True)
    # This is just to set the right order of the output columns
    processed_cat = processed_cat[['id_subcube', 'ra', 'dec', 'hi_size', 'line_flux_integral', 'central_freq', 'pa', 'i', 'w20', 'rms', 'subcube']]
    processed_cat['central_freq'] = processed_cat['central_freq'].map('{:.1f}'.format)
    return processed_cat

def find_fitsfile(parfile):
    """ Searchs in the parfile the name of the fits file used"""
    with open(parfile, 'r') as f:
        for line in f.readlines():
            if 'input.data' in line:
                break
        fitsfile = line.split('=')[1].strip()
    return fitsfile


def main():
    args = get_args()
    output_path = os.path.join(args.results_path, args.outname)
#    output_catalog = os.path.join(output_path, f'{args.outname}_{args.datacube}_cat.txt')
#    raw_cat = sofia2cat(catalog=output_catalog)
    incatalog = args.incatalog
    raw_cat = sofia2cat(catalog=incatalog)
    fitsfile = find_fitsfile(os.path.join(output_path, 'sofia.par'))
    processed_cat = process_catalog(raw_cat, fitsfile)
    final_cat_file = incatalog.replace('_cat.txt', '_final_catalog.csv')
#    final_cat_file = os.path.join(output_path, 'final_catalog.csv')
    processed_cat.to_csv(final_cat_file, sep=' ', index=False)

if __name__ == '__main__':
    main()

