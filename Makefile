.PHONY: setup lint format test serve migrate build jmeter postman

setup:
	pip install -U pip
	pip install -r requirements.txt

lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy app

format:
	black .
	isort .

test:
	pytest -q --cov=app --cov-report=term-missing --cov-report=xml --cov-fail-under=80

serve:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

migrate:
	alembic upgrade head

build:
	python -m pip install build
	python -m build

postman:
	newman run postman/biblioteca.postman_collection.json

jmeter:
	./apache-jmeter-5.6.3/bin/jmeter -n -t jmeter/api_books.jmx -l jmeter/results.jtl -e -o jmeter/report
