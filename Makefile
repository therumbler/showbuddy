.PHONY: setup-python test test-unit test-integration

VENV := .venv

setup-python:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@. $(VENV)/bin/activate && echo "Virtual environment activated."
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

test-integration:
	python3 -m unittest tests/integration/*.py

test-unit:
	python3 -m unittest tests/unit/*.py

test: test-unit test-integration

