.PHONY: help install lint format check test clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make lint       - Run linter (Ruff)"
	@echo "  make format     - Format code (Ruff)"
	@echo "  make check      - Check code without fixing (lint + format check)"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean cache files"

install:
	uv sync

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

check:
	uv run ruff check .
	uv run ruff format --check .

test:
	uv run pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
