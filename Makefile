SHELL := bash
.SHELLFLAGS := -euo pipefail -c

install:
	pipenv install

install-dev:
	pipenv install --dev

test:
	pipenv run pytest --cov-config=.coveragerc --cov=. --cov-report=xml

lint:
# stop the build if there are Python syntax errors or undefined names
	pipenv run flake8  . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	pipenv run flake8  . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

