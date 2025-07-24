check-coverage:
	pytest --cov=. --cov-fail-under=80 tests/


install:	
	poetry install


test:
	poetry run pytest

