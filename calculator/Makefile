.PHONY: venv install test clean run test-coverage

venv:
	uv venv

install:
	uv sync

test:
	uv run pytest test_calculator.py

test-coverage:
	uv run pytest --cov=pkg test_calculator.py

clean:
	rm -rf .venv
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

run:
	uv run python main.py
