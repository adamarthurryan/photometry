import matplotlib.pyplot as plt
from astropy.time import Time
from collections import defaultdict
from collections import namedtuple, defaultdict
from itertools import cycle

import os

def plot_light_curves(results, output_dir):
    data_by_filter = defaultdict(list)

    for r in results:
        if r['mag'] is not None:
            data_by_filter[r['filter']].append(r)

    # create a named tuple to hold plot data
    PlotData = namedtuple('PlotData', ['type', 'dates', 'observations'])

    # create an associative array of data items 
    # with the name as the key
    plots = dict()

    for f, data in data_by_filter.items():

        for r in data:
            t = r['date']

            if r['name'] not in plots:
                plots[r['name']] = PlotData(
                    type=r['type'],
                    dates=[],
                    observations=[]
                )
            
            plots[r['name']].dates.append(r['date'])
            plots[r['name']].observations.append({
                'mag': r['mag'],
                'snr': r['snr'],
                # Calculate error based on SNR  
                'err': 1.0857 / r['snr'] if r['snr'] > 0 else 0.1
            })
            

        plt.figure(figsize=(10, 6))

        # random colors cf. https://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib 
        cycol = cycle('bgrcmk')
        cyfmt = cycle('ov^sD')


        for name in plots.keys():
            
            # Skip comparison stars
            if plots[name].type == 'comparison':    
                continue
            
            mags = []
            errs = []

            plot_data = plots[name]
            times = plot_data.dates
            for obs in plot_data.observations:
                mags.append(obs['mag'])
                errs.append(obs['err'])
            
            plt.errorbar(times, mags, yerr=errs, fmt=next(cyfmt), label=name, color=next(cycol), capsize=3)

        plt.gca().invert_yaxis()
        plt.xlabel("Julian Date")
        plt.ylabel("Magnitude")
        plt.title(f"Light Curve ({f}-band)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plot_path = os.path.join(output_dir, f"light_curve_{f}.png")
        plt.savefig(plot_path)
        print(f"Saved light curve: {plot_path}")
        plt.close()
