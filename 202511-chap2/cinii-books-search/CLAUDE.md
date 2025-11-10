# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python 3.13 project for CiNii Books search functionality, managed with uv (fast Python package manager).

## Package Management

This project uses **uv** instead of pip/poetry:
- Install dependencies: `uv sync`
- Add a dependency: `uv add <package>`
- Add a dev dependency: `uv add --dev <package>`
- Run Python scripts: `uv run python main.py` or `uv run main.py`

## Development Commands

### Code Quality
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Type check**: `uv run mypy .`

### Testing
- **Run tests**: `uv run pytest`
- **Run specific test**: `uv run pytest path/to/test_file.py::test_function_name`
- **Run with verbose output**: `uv run pytest -v`

### Running the Application
- **Main entry point**: `uv run python main.py`

## Project Structure

Currently minimal structure with:
- `main.py` - Main application entry point
- `pyproject.toml` - Project configuration and dependencies
- `.venv/` - Virtual environment (managed by uv)

## Python Environment

- Python version: 3.13 (specified in `.python-version`)
- Virtual environment is automatically managed by uv
- pythonコマンドは `uv run python` から実行し、Pythonでは標準ライブラリのみを利用する。