import json
import os
from typing import Dict
from urllib.parse import urlparse

import humanize
import requests


def get_id_from_tmdb_url(tmdb_url: str) -> int:
    parsed_url = urlparse(tmdb_url)
    path_with_id = parsed_url.path.rpartition("/")[2]
    tmdb_id = path_with_id.split("-")[0]

    return int(tmdb_id)


def process_verse(verse: str) -> str:
    if verse.startswith("Ecclesiasticus"):
        return verse.replace("Ecclesiasticus", "Sirach")
    elif verse.startswith("Corinthians"):
        return verse.replace("Corinthians", "1 Corinthians")
    else:
        return verse


TV_SHOW_URL: str = "https://www.themoviedb.org/tv/87689-warrior-nun"
TV_SHOW_ID: int = get_id_from_tmdb_url(TV_SHOW_URL)

BASE_URL: str = "https://api.themoviedb.org/3"
# HEADERS: Dict[str, str] = {"Authorization": f"Bearer {os.environ['TMDB_API_KEY']}"}

# https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression
BASE_PARAMS: Dict[str, str] = {"api_key": os.environ["TMDB_API_KEY"]}
PARAMS: Dict[str, str] = {**BASE_PARAMS, "language": "pt-PT"}

BIBLE_API_BASE_URL: str = "https://bible-api.com"

if __name__ == "__main__":
    # https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
    # https://developers.themoviedb.org/3/getting-started/languages
    # https://developers.themoviedb.org/3/getting-started/authentication

    url = f"{BASE_URL}/tv/{TV_SHOW_ID}"

    r = requests.get(url, params=BASE_PARAMS)
    data = r.json()

    n_seasons = data["number_of_seasons"]

    output = []
    for season in range(1, n_seasons + 1):
        url = f"{BASE_URL}/tv/{TV_SHOW_ID}/season/{season}"

        r = requests.get(url, params=BASE_PARAMS)
        data = r.json()

        for episode in data["episodes"]:
            # https://en.wikipedia.org/wiki/Book_of_Sirach
            # https://warriornun.fandom.com/wiki/Ecclesiasticus_26:9-10
            # https://ebible.org/web/SIR01.htm
            # https://github.com/seven1m/open-bibles
            # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-details
            verse = episode["name"]

            r = requests.get(
                f"{BIBLE_API_BASE_URL}/{process_verse(verse)}",
                params={"translation": "web"},
            )
            data = r.json()

            try:
                verse_text = data["text"].strip()
            except KeyError:
                verse_text = None

            output.append(
                {
                    "season": season,
                    "episode": episode["episode_number"],
                    "title": verse,
                    "verse_text": verse_text,
                }
            )

    # https://github.com/typicode/demo
    # https://github.com/typicode/demo/blob/master/db.json
    # https://my-json-server.typicode.com/pricing
    # https://github.com/python-humanize/humanize#file-size-humanization
    # https://superuser.com/questions/66825/what-is-the-difference-between-size-and-size-on-disk
    # print(output)
    with open("db.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print(f"Size: {humanize.naturalsize(os.path.getsize('db.json'))}")
    print("All done!")
