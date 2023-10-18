#!venv/bin/python3

from modules import oikotie
from modules import etuovi

import csv


def save_csv(listings):
    print ("saving")
    with open("listings.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        fieldnames = ["X", "Y", "fid", "name", "hinta", "url"]
        writer.writerow(fieldnames)
        for idx, row in enumerate(listings):
            row_with_fid = [row[0], row[1], idx, row[2], row[3], row[4]]
            writer.writerow(row_with_fid)


def CasaEx():
    """DEFAULT PARAMETERS commented out for easy copying
    basic_parameters = {
        # maximum price
        "maximum_price": 300000,
        # acceptable amount of rooms
        "rooms": [5, 6, 7],
        # minimum floor area in squaremeters
        "minimum_area": 120,
        # keywords
        "keywords": [""],
        # has sauna
        "sauna": True,
    }
    """
    basic_parameters = {
        # maximum price
        "maximum_price": 300000,
        # acceptable amount of rooms
        "rooms": [5, 6, 7],
        # minimum floor area in squaremeters
        "minimum_area": 120,
        # keywords
        "keywords": [],
        # has sauna
        "sauna": True,
    }
    data = []

    # comment out the unneeded modules
    sources = [
        lambda params: oikotie.fetch_data(params),
        lambda params: etuovi.fetch_data(params),
    ]

    for source in sources:
        listing_data = source(basic_parameters)

        data.extend(checker(data, listing_data))
        #data.extend(listing_data)
        

    save_csv(data)

"""
def read_csv():
    with open("listings.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        listings = []
        for row in reader:
            listings.append(row)

        return listings
"""

def check_duplicate_address(A, B):
    from difflib import SequenceMatcher

    result = SequenceMatcher(None, A, B).ratio()

    if result >= 0.8:
        print (f"dupe: {A} and {B}")
        return True
    return False

def checker(data, new_data):
    
    not_dupe = []
    if not data:
        not_dupe.extend(new_data)
    else:
        for d in new_data:
            if not any(check_duplicate_address(d[2], y[2]) for y in data):
                not_dupe.append(d)               
       
    return not_dupe

if __name__ == "__main__":
    CasaEx()
    #dev()
