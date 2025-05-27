# Photometry Tool

This is a command-line Python tool for performing aperture photometry on FITS images using WCS coordinates.

## Features
- Command line interface
- YAML-based configuration for star sequences
- Multi-filter support
- Light curve generation and plotting

## Usage
```bash
python -m photometry_tool --config example_data/series.yaml example_data/*.fits
```

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
```