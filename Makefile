lint:
	black . && isort . && flake8

coverage:
	coverage run -m pytest
