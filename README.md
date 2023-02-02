# warrior-nun-db

> https://my-json-server.typicode.com/joaopalmeiro/warrior-nun-db

## Development

```bash
cp .env.example .env
```

Add your [TMDB's API key](https://developers.themoviedb.org/3/getting-started/introduction) to the `.env` file.

```bash
pipenv install --dev
```

```bash
pipenv shell
```

```bash
python script.py
```

```bash
isort --profile black script.py && black script.py
```

```bash
mypy script.py
```

## Notes

- https://github.com/celiao/tmdbsimple
- `pipenv --python 3.7`
- `pipenv install httpx humanize && pipenv install --dev black isort mypy`
- `exit && pipenv --rm` (https://github.com/pypa/pipenv/issues/4942)
- https://docs.pipenv.org/advanced/#automatic-loading-of-env
- https://bible-api.com/
- https://en.wikipedia.org/wiki/World_English_Bible
- https://en.wikipedia.org/wiki/Open_English_Bible
- https://en.wikipedia.org/wiki/Bible_in_Basic_English
- https://www.themoviedb.org/documentation/api
- https://my-json-server.typicode.com/
- https://mypy.readthedocs.io/en/stable/
