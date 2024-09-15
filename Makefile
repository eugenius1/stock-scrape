SHELL := bash
.SHELLFLAGS := -euo pipefail -c

install:
	pipenv install

install-dev:
	pipenv install --dev

test:
	pipenv run pytest --cov=scraper

run:
	pipenv run python main.py
