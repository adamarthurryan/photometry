import argparse
import glob

def parse_args():
    parser = argparse.ArgumentParser(description="Photometry Tool with WCS and multi-filter support")
    parser.add_argument('images', nargs='+', help='FITS image file patterns (e.g., *.fits)')
    parser.add_argument('--config', required=True, help='YAML config with star definitions')
    parser.add_argument('--graph', default=False, action='store_true', help='Generate light curve plots')
    parser.add_argument('--output', default='photometry_results.csv', help='CSV output path')
    parser.add_argument('--output-dir', default='output', help='Directory to save light curve plots')
    args = parser.parse_args()

    # Expand globs
    expanded = []
    for pattern in args.images:
        expanded.extend(glob.glob(pattern))
    if not expanded:
        raise ValueError("No FITS files matched.")
    args.images = sorted(set(expanded))

    return args
