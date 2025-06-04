# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project called "quicktoken" using modern Python packaging with pyproject.toml and uv for dependency management.

## Common Commands

### Running the Application
```bash
python main.py
```

### Dependency Management (using uv)
```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Install all dependencies
uv sync

# Run commands in the virtual environment
uv run python main.py
```

### Virtual Environment
- Virtual environment is located at `/.venv/` and is already activated
- Use `uv` for all Python dependency and virtual environment management
- Do not use pip, pipenv, poetry, or other tools

## Project Structure

- `main.py` - Main entry point with basic hello world functionality
- `pyproject.toml` - Python project configuration and metadata
- `README.md` - Currently empty project documentation

## Development Notes

- Always use `uv` commands for dependency management
- Virtual environment is pre-configured and active
- No testing framework, linting, or formatting tools are currently configured