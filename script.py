import asyncio
import itertools
import json
import os
from typing import Dict, List, Union
from urllib.parse import urlparse

import humanize
from httpx import AsyncClient


def get_id_from_tmdb_url(tmdb_url: str) -> int:
    parsed_url = urlparse(tmdb_url)
    path_with_id = parsed_url.path.rpartition("/")[2]
    tmdb_id = path_with_id.split("-")[0]

    return int(tmdb_id)


def process_verse(verse: str) -> str:
    # https://en.wikipedia.org/wiki/Book_of_Sirach
    # https://warriornun.fandom.com/wiki/Ecclesiasticus_26:9-10
    # https://ebible.org/web/SIR01.htm
    # https://github.com/seven1m/open-bibles
    # https://developers.themoviedb.org/3/tv-seasons/get-tv-season-details
    if verse.startswith("Ecclesiasticus"):
        return verse.replace("Ecclesiasticus", "Sirach")
    elif verse.startswith("Corinthians"):
        return verse.replace("Corinthians", "1 Corinthians")
    else:
        return verse


async def get_seasons(client: AsyncClient, url: str) -> int:
    r = await client.get(url, params=BASE_PARAMS)
    data = r.json()
    # print(type(client), type(data["number_of_seasons"]))

    return data["number_of_seasons"]


async def get_episode_output(
    client: AsyncClient, verse: str, episode: int, season: int
) -> Dict[str, Union[str, int, None]]:
    # https://stackoverflow.com/questions/39429526/how-to-specify-nullable-return-type-with-type-hints
    url = f"{BIBLE_API_BASE_URL}/{process_verse(verse)}"
    r = await client.get(url, params={"translation": BIBLE_TRANSLATION})
    data = r.json()

    # print(type(episode), type(season))

    try:
        # verse_text = data["text"]
        verse_text = data["text"].strip()
    except KeyError:
        verse_text = None

    return {
        "season": season,
        "episode": episode,
        "title": verse,
        "verse_text": verse_text,
    }


async def get_episodes(
    client: AsyncClient, url: str
) -> List[Dict[str, Union[str, int, None]]]:
    r = await client.get(url, params=BASE_PARAMS)
    data = r.json()
    # print(type(data["episodes"]), type(data["episodes"][0]))

    tasks = []
    for episode in data["episodes"]:
        verse = episode["name"]
        tasks.append(
            asyncio.ensure_future(
                get_episode_output(
                    client, verse, episode["episode_number"], episode["season_number"]
                )
            )
        )

    outputs = await asyncio.gather(*tasks)
    # print(type(outputs))
    return outputs


TV_SHOW_URL: str = "https://www.themoviedb.org/tv/87689-warrior-nun"
TV_SHOW_ID: int = get_id_from_tmdb_url(TV_SHOW_URL)

BASE_URL: str = "https://api.themoviedb.org/3"
# HEADERS: Dict[str, str] = {"Authorization": f"Bearer {os.environ['TMDB_API_KEY']}"}

# https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression
BASE_PARAMS: Dict[str, str] = {"api_key": os.environ["TMDB_API_KEY"]}
# PARAMS: Dict[str, str] = {**BASE_PARAMS, "language": "pt-PT"}

BIBLE_API_BASE_URL: str = "https://bible-api.com"
BIBLE_TRANSLATION: str = "web"
# BIBLE_TRANSLATION: str = "bbe"
# BIBLE_TRANSLATION: str = "kjv"
# BIBLE_TRANSLATION: str = "oeb-us"
# BIBLE_TRANSLATION: str = "webbe"


async def main() -> None:
    # https://www.python-httpx.org/async/
    # https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-httpx-and-asyncio
    async with AsyncClient() as client:
        # https://developers.themoviedb.org/3/tv/get-tv-details
        url = f"{BASE_URL}/tv/{TV_SHOW_ID}"
        n_seasons = await get_seasons(client, url)
        # print(n_seasons)

        tasks = []
        for season in range(1, n_seasons + 1):
            url = f"{BASE_URL}/tv/{TV_SHOW_ID}/season/{season}"
            tasks.append(asyncio.ensure_future(get_episodes(client, url)))

        episodes = await asyncio.gather(*tasks)

    with open("db.json", "w") as f:
        json.dump(
            {"en": list(itertools.chain.from_iterable(episodes))},
            f,
            ensure_ascii=False,
            indent=4,
        )


if __name__ == "__main__":
    # https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
    # https://developers.themoviedb.org/3/getting-started/languages
    # https://developers.themoviedb.org/3/getting-started/authentication

    asyncio.run(main())

    # https://github.com/typicode/demo
    # https://github.com/typicode/demo/blob/master/db.json
    # https://my-json-server.typicode.com/pricing
    # https://github.com/python-humanize/humanize#file-size-humanization
    # https://superuser.com/questions/66825/what-is-the-difference-between-size-and-size-on-disk
    print(f"Size: {humanize.naturalsize(os.path.getsize('db.json'))}")
    print("All done!")
