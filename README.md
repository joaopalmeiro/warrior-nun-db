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

## Notes

- https://github.com/celiao/tmdbsimple
- `pipenv --python 3.7`
- `pipenv install requests humanize && pipenv install --dev black isort`
- https://docs.pipenv.org/advanced/#automatic-loading-of-env
- https://bible-api.com/
- https://www.themoviedb.org/documentation/api
- https://my-json-server.typicode.com/
