SHELL := bash
.SHELLFLAGS := -euo pipefail -c

install:
	pipenv install

test:
	pipenv run python -m unittest discover .
