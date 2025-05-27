from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u


def has_wcs(fits_file):
    with fits.open(fits_file) as hdul:
        wcs = WCS(hdul[0].header)


def compute_star_pixel_positions(fits_file, stars):
    with fits.open(fits_file) as hdul:
        wcs = WCS(hdul[0].header)
    
    positions = []
    for s in stars:
        coord = SkyCoord(ra=s['ra'] * u.deg, dec=s['dec'] * u.deg, frame='icrs')
        x, y = wcs.world_to_pixel(coord)
        positions.append({
            **s, 'x': x, 'y': y
        })
    return positions
