test-integration:
	python3 -m unittest tests/integration/*.py

test-unit:
	python3 -m unittest tests/unit/*.py

test: test-unit test-integration
