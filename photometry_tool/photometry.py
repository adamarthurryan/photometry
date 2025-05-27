from astropy.io import fits
from astropy.time import Time
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
import numpy as np
from astropy.table import Table

def do_photometry(fits_file, stars, aperture_radius=5, annulus_radii=(8, 12)):
    with fits.open(fits_file) as hdul:
        data = hdul[0].data
        header = hdul[0].header

    obs_time = Time(header.get('DATE-OBS', 'UNKNOWN')).jd

    filter_band = header.get('FILTER', 'V').upper()

    results = []

    fluxes = {}
    for s in stars:
        pos = (s['x'], s['y'])
        ap = CircularAperture(pos, r=aperture_radius)
        ann = CircularAnnulus(pos, *annulus_radii)

        phot = aperture_photometry(data, [ap, ann])
        bkg_mean = phot['aperture_sum_1'][0] / ann.area
        bkg_total = bkg_mean * ap.area
        flux = phot['aperture_sum_0'][0] - bkg_total

        #is this the right way to calculate SNR?
        snr = flux / np.sqrt(abs(flux)) if flux > 0 else 0

        fluxes[s['name']] = flux
        results.append({
            'date': obs_time,
            'filter': filter_band,
            'name': s['name'],
            'type': s['type'],
            'flux': flux,
            'snr': snr,
            'known_mag': s.get('magnitudes', {}).get(filter_band)
        })

    comps = [r for r in results if r['type'] == 'comparison' and r['flux'] > 0 and r['known_mag']]
    if not comps:
        raise ValueError ("Comparison star not detected.")
    
    zp = np.mean([r['known_mag'] + 2.5 * np.log10(r['flux']) for r in comps]) if comps else 0

    for r in results:
        r['mag'] = -2.5 * np.log10(r['flux']) + zp if r['flux'] > 0 else None
        r['check_dev'] = r['mag'] - r['known_mag'] if r['type'] == 'check' and r['known_mag'] and r['mag'] else None

    return results

def build_result_table(results):
    return Table(rows=[
        {
            'date': r['date'],
            'filter': r['filter'],
            'name': r['name'],
            'type': r['type'],
            'mag': round(r['mag'], 4) if r['mag'] else None,
            'snr': round(r['snr'], 2),
            'check_dev': round(r['check_dev'], 4) if r['check_dev'] else None
        } for r in results
    ])
