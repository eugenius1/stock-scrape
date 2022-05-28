SHELL := bash
.SHELLFLAGS := -euo pipefail -c

test:
	python -m unittest discover .
