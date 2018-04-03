import requests


def load_page(url: str):
    response = requests.get(url)
    if not response.ok:
        raise ConnectionError("Response not ok", response.status_code, url)
    return response.content
