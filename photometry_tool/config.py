import yaml

def load_star_config(filepath):
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    stars = data.get('stars', [])
    for s in stars:
        if not all(k in s for k in ('name', 'type', 'ra', 'dec')):
            raise ValueError(f"Missing required fields in star: {s}")
        if s['type'] not in {'target', 'comparison', 'check'}:
            raise ValueError(f"Invalid star type: {s['type']}")
    return stars
