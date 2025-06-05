# Getting Started

This guide helps new contributors set up a local Fundalyze environment.

## Prerequisites
- **Python 3.11** or later
- **Git** and a recent version of **pip**

## Setup Steps
1. Fork and clone the repository.
2. Run `./bootstrap_env.sh` (or `bootstrap_env.ps1` on Windows). This creates
   `.venv` and installs all dependencies from `requirements.txt`.
3. Copy `config/.env` from the example below and fill in your API keys.
4. Run `python scripts/main.py` to open the interactive menu.

## Example `.env`
```env
OPENBB_TOKEN=your-openbb-key
FMP_API_KEY=your-fmp-key
DIRECTUS_URL=https://your-directus.example.com
DIRECTUS_API_TOKEN=secret-token
OUTPUT_DIR=output
```
See [configuration.md](configuration.md) for the full list of optional
variables and detailed explanations.

## Running Tests
Activate the virtual environment and execute:
```bash
pytest -q
```
All tests should pass before submitting a pull request.
