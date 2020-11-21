# Generate thumbnails and metadata for photos

I've configured and am running this project with `pipenv` to make things easier. The following instructions are `pipenv` specific. Python 3 is also required for this project, and I have personally tested it with 3.7 and 3.8.

## Install the dependencies

```
pipenv install
```

## Generate thumbnails

```
pipenv run python3 main.py /path/to/Photos/
```

Outputs generated thumbnails to `/path/to/Photos Thumbnails/`

## Generate metadata

```
pipenv run python3 metadata.py /path/to/Photos/
```

Outputs generated metadata file to `/path/to/Photos Metadata.json`
