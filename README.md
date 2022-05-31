# Ants

This is being built with [poetry](https://python-poetry.org/).

## Install

Poetry, by default, installs the Python environment in a cache folder somewhere where it will be lost, occupying space on your disk. I recommend running

```sh
$ poetry config virtualenvs.in-project true  
```

so that the Python environment is installed in the same folder as the project, in a folder called `.venv`.

```sh
# to install the dependencies
$ poetry install
```

## Run

```sh
$ poetry run start
```
