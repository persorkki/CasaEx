"""This module fetches house listings from etuovi.com"""
import requests
from modules.headers import base_headers
DETAIL_URL = "https://www.etuovi.com/api/v2/announcement/details"
TARGET_URL = "https://www.etuovi.com/kohde/"
URL = "https://www.etuovi.com/api/v2/announcements/search/listpage"


def _transform_parameters(basic_parameters):
    # transform maximum price
    maximum_price = basic_parameters["maximum_price"]

    # transform room count
    translated_rooms = [
        "ONE_ROOM",
        "TWO_ROOMS",
        "THREE_ROOMS",
        "FOUR_ROOMS",
        "FIVE_ROOMS",
        "MORE_THAN_FIVE_ROOMS",
    ]
    rooms = []
    for room in basic_parameters["rooms"]:
        if room > len(translated_rooms):
            if translated_rooms[-1] in rooms:
                continue
        else:
            rooms.append(translated_rooms[room - 1])

    minimum_area = basic_parameters["minimum_area"]
    has_sauna = basic_parameters["sauna"]
    keywords = " ".join(basic_parameters["keywords"])
    params = {
        "apartmentHasSauna": has_sauna,
        "bidType": "ALL",
        "freeTextSearch": keywords,
        "hasShore": True,
        "locationSearchCriteria": {
            "classifiedLocationTerms": [],
            "unclassifiedLocationTerms": [],
        },
        "maintenanceChargeMax": None,
        "maintenanceChargeMin": None,
        "newBuildingSearchCriteria": "ALL_PROPERTIES",
        "officesId": [],
        "ownershipTypes": ["OWN"],
        "pagination": {
            "firstResult": 0,
            "maxResults": 100,
            "page": 1,
            "sortingOrder": {
                "direction": "DESC",
                "property": "PUBLISHED_OR_UPDATED_AT",
            },
        },
        "plotAreaMax": None,
        "plotAreaMin": None,
        "priceMax": maximum_price,
        "priceMin": None,
        "priceSquareMeterMax": None,
        "priceSquareMeterMin": None,
        "propertyType": "RESIDENTIAL",
        "publishingTimeSearchCriteria": "ANY_DAY",
        "residentialPropertyTypes": ["DETACHED_HOUSE"],
        "roomCounts": rooms,
        "sellerType": "ALL",
        "showingSearchCriteria": {},
        "sizeMax": None,
        "sizeMin": minimum_area,
        "yearMax": None,
        "yearMin": None,
    }
    return params


def _get_headers():
    # get base headers
    headers = base_headers

    # add host
    headers.update({"Host": "www.etuovi.com"})
    headers.update({"Content-Type": "application/json"})

    # tokens and cookie
    # TODO: get a new token at the start of this module
    headers.update({"X-XSRF-TOKEN": "4d28cdcf-d2d1-40a0-a6c0-e8d75eee01a1"})
    headers.update(
        {
            "Cookie": "uuidc=9da0ecf6-7f9f-43b1-b895-9581f8b127c5; sammio-bsid=584b1f45-1847-4ffb-a23f-1da7cd765213; sammio-init-time=2023-08-16T20:27:37.276Z; XSRF-TOKEN=4d28cdcf-d2d1-40a0-a6c0-e8d75eee01a1; SESSION=772fb57a-a196-4d05-9e8b-8a19eec960d3"
        }
    )
    return headers


def fetch_data(basic_parameters):
    headers = _get_headers()
    params = _transform_parameters(basic_parameters)

    response = requests.post(URL, json=params, headers=headers, timeout=10)

    if not response.ok:
        print("Error - could not add listings from Etuovi")
        return []

    data = response.json()
    total_count = data["countOfAllResults"]
    listings = []
    #TODO: this could maybe import a utility class that handles printing the name and the iteration
    print("--- [etuovi.com] ---")
    for idx, card in enumerate(data["announcements"]):
        print(f"+ {idx+1}/{total_count}")

        # id for detailed search and listing specific url
        friendlyId = card["friendlyId"]

        # coords
        [x, y] = _get_coords(friendlyId)
        if (x, y) == (0, 0):
            print(f"Unable to fetch coords for listing {card['location']}")
            continue

        # address
        address = card["addressLine1"]

        # asking price
        price = f"{card['searchPrice']} €"

        # listing specific url
        url = TARGET_URL + friendlyId

        listings.append([x, y, address, price, url])

    return listings


def _get_coords(friendlyId: str):
    """gets coordinates for a listing, returns a tuple. returns a tuple of (0,0) on fetch error"""
    params = {
        "friendlyId": friendlyId,
    }
    res = requests.get(DETAIL_URL, params=params, timeout=10)
    if res.ok:
        data = res.json()
        x = data["property"]["geoCode"]["longitude"]
        y = data["property"]["geoCode"]["latitude"]
        return (x, y)
    return (0, 0)


if __name__ == "__main__":
    pass
