# CasaEx - Home Explorer
### A utility for scouring real estate websites in search of property listings and converting them into a format compatible with QGIS.

### Currently only has some very basic search filtering and only has two modules (real estate websites) by default

## Requirements
- Python 3+
- `requests` python library
- `beautifulsoup4` python library

## Installation
- `pip install -r requirements.txt`

## Usage
Running the script `CasaEx.py` outputs a CSV file called `listings.csv` which has the listing information in the following format: `x, y, fid, address, price`