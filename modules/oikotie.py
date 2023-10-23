"""This module fetches house listings from oikotie.fi"""
import requests
from bs4 import BeautifulSoup
from modules.headers import base_headers


def _get_headers():
    # get base headers
    headers = base_headers
    # add OTA tokens to headers
    headers.update(_get_tokens(headers))
    # and host
    headers.update({"Host": "asunnot.oikotie.fi"})
    return headers


def _get_tokens(headers: dict[str, str]) -> dict[str, str]:
    """sets OTA-tokens to headers that are needed for the search to function"""

    token_base_url = "https://asunnot.oikotie.fi"

    res = requests.get(token_base_url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    meta_token = soup.find("meta", {"name": "api-token"})
    api_token = meta_token["content"] if meta_token else None  # type: ignore

    meta_loaded = soup.find("meta", {"name": "loaded"})
    loaded = meta_loaded["content"] if meta_loaded else None  # type: ignore

    meta_cuid = soup.find("meta", {"name": "cuid"})
    cuid = meta_cuid["content"] if meta_cuid else None  # type: ignore

    if api_token and loaded and cuid:
        return {
            "OTA-token": api_token,
            "OTA-loaded": loaded,
            "OTA-cuid": cuid,
        }  # type: ignore
    return {}


def _transform_parameters(basic_parameters):
    maximum_price = basic_parameters["maximum_price"]
    rooms = basic_parameters["rooms"]
    minimum_area = basic_parameters["minimum_area"]
    keywords = basic_parameters["keywords"]
    sauna = []
    if basic_parameters["sauna"]:
        sauna.append(2)

    params = {
        "buildingType[]": [4, 8, 32, 128],
        "cardType": 100,
        "limit": 1000,
        "offset": 0,
        "price[max]": maximum_price,
        "roomCount[]": rooms,
        "shoreOwnershipType[]": sauna,
        "size[min]": minimum_area,
        "sortBy": "published_sort_desc",
        "keywords[]": keywords,
    }
    return params


def fetch_data(basic_parameters):
    headers = _get_headers()
    params = _transform_parameters(basic_parameters)

    base_url = "https://asunnot.oikotie.fi/api/search"

    response = requests.get(base_url, headers=headers, params=params, timeout=10)
    listings = []
    if response.status_code == 200:
        data = response.json()
        total_count = data["found"]
        print("--- [oikotie.fi] ---")
        for idx, card in enumerate(data["cards"]):
            print(f"+ {idx+1}/{total_count}")
            address = card["location"]["address"]
            x = card["location"]["longitude"]
            y = card["location"]["latitude"]
            price = card["data"]["price"].replace("\xa0", "").replace("€", " €")
            url = card["url"]
            listing = [x, y, address, price, url]
            listings.append(listing)
    return listings


if __name__ == "__main__":
    pass
