import requests
import csv
from bs4 import BeautifulSoup

headers = {
    "Host": "asunnot.oikotie.fi",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}

def _set_tokens(headers: dict[str, str]) -> dict[str,str] | None:
    """sets OTA-tokens to headers that are needed for the search to function"""

    token_base_url = "https://asunnot.oikotie.fi"

    res = requests.get(token_base_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    meta_token = soup.find("meta", {"name": "api-token"})
    api_token = meta_token["content"] if meta_token else None  # type: ignore

    meta_loaded = soup.find("meta", {"name": "loaded"})
    loaded = meta_loaded["content"] if meta_loaded else None  # type: ignore

    meta_cuid = soup.find("meta", {"name": "cuid"})
    cuid = meta_cuid["content"] if meta_cuid else None  # type: ignore

    if api_token and loaded and cuid:
        headers["OTA-token"] = api_token  # type: ignore
        headers["OTA-loaded"] = loaded  # type: ignore
        headers["OTA-cuid"] = cuid  # type: ignore
        return headers
    
    raise AttributeError("OTA -headers could not be set")

def fetch_data():
    # TODO: base headers should probably be coming from the caller
    headers = {
        "Host": "asunnot.oikotie.fi",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
    }

    headers = _set_tokens(headers)
    base_url = "https://asunnot.oikotie.fi/api/search"

    params = {
        "buildingType[]": [4, 8, 32, 128],
        "cardType": 100,
        "limit": 1000,
        "offset": 0,
        "price[max]": 300000,
        "roomCount[]": [5, 6, 7],
        "shoreOwnershipType[]": [2, 16],
        "size[min]": 120,
        "sortBy": "published_sort_desc"
    }

    response = requests.get(base_url, headers=headers, params=params)
    listings = []
    if response.status_code == 200:
        data = response.json()
        for idx,card in enumerate(data["cards"]):
            address = card["location"]["address"]
            x = card["location"]["longitude"]
            y = card["location"]["latitude"]
            price = card["data"]["price"]
            url = card["url"]
            listing = [
                x,
                y,
                idx,
                address,
                price,
                url
            ]
            listings.append(listing)
    return listings


if __name__ == "__main__":
    pass
