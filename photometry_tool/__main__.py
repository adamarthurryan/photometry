from .cli import parse_args
from .config import load_star_config
from .wcs_utils import compute_star_pixel_positions
from .photometry import do_photometry, build_result_table
from .plotter import plot_light_curves

def main():
    args = parse_args()
    stars = load_star_config(args.config)

    all_results = []
    for fits_file in args.images:
        print(f"\nProcessing {fits_file}...")
        
        #try and get star positions and show a message if it fails
        try:
            star_positions = compute_star_pixel_positions(fits_file, stars)
        except Exception as e:
            print(f"Error computing star positions: {e}")
            continue
        try:
            results = do_photometry(fits_file, star_positions)
        except Exception as e:
            print(f"Error performing photometry: {e}")
            continue

        all_results.extend(results)

    table = build_result_table(all_results)
    table.write(args.output, format='csv', overwrite=True)
    print(f"\nSaved photometry results to: {args.output}")

    if args.graph:
        plot_light_curves(all_results, args.output_dir)

if __name__ == "__main__":
    main()
