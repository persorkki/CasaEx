#!venv/bin/python3

import csv
from difflib import SequenceMatcher

from modules import oikotie
from modules import etuovi


def save_csv(listings):
    """writes the data into a csv file"""
    print("saving")
    with open("listings.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        fieldnames = ["X", "Y", "fid", "name", "hinta", "url"]
        writer.writerow(fieldnames)
        for idx, row in enumerate(listings):
            row_with_fid = [row[0], row[1], idx, row[2], row[3], row[4]]
            writer.writerow(row_with_fid)


def CasaEx():
    """main function"""
    basic_parameters = {
        # maximum price
        "maximum_price": 300000,  # default: 300000
        # acceptable amount of rooms
        "rooms": [5, 6, 7],  # default: [5, 6, 7]
        # minimum floor area in squaremeters
        "minimum_area": 120,  # default: 120
        # keywords
        "keywords": [],  # default: []
        # has sauna
        "sauna": True,  # default: True
    }
    data = []

    # add/remove modules here:
    modules = [
        oikotie,
        etuovi
    ]

    sources = []
    for module in modules:
        sources.append(module.fetch_data) if hasattr(module, "fetch_data") else None

    for src in sources:
        listing_data = src(basic_parameters)
        data.extend(checker(data, listing_data))

    save_csv(data)


def check_duplicate_address(A, B):
    """compares two values and returns if their difference matches the tolerance"""
    from difflib import SequenceMatcher

    result = SequenceMatcher(None, A, B).ratio()
    if result >= 0.8:
        print(f"dupe: {A} and {B}")
        return True
    return False


def checker(data, new_data):
    """compares two data sources and finds duplicates"""
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
    # dev()
