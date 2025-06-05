# Contributing to Fundalyze

Thank you for helping improve Fundalyze! This document explains how to get a development environment running and the workflow for submitting changes.

## Getting Started

1. **Fork** the repository on GitHub and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/Fundalyze.git
   cd Fundalyze
   ```
2. **Set up Python** using the bootstrap script or manually:
   ```bash
   ./bootstrap_env.sh      # macOS/Linux
   .\bootstrap_env.ps1     # Windows PowerShell
   ```
   This creates a `.venv` directory and installs dependencies from `requirements.txt`.

   If you prefer manual setup:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   Fundalyze does not require Node.js, but if you add JS tooling make sure to install Node and run `npm install` in the relevant directory.

## Code Style

- **Python**: follow [PEP 8](https://peps.python.org/pep-0008/). Use `black` and `isort` before committing.
- **JavaScript** (if used): run `prettier` and `eslint`.

## Running Tests

Run the full test suite with:
```bash
pytest -q
```
All tests should pass before opening a pull request. You can also run `scripts/run_tests.py` to execute each test file sequentially.

## Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make your edits and commit with a concise message:
   ```bash
   git commit -am "Add portfolio export command"
   ```
3. Push your branch and open a pull request against `main` on GitHub.

### Pull Request Template

Include the following information in your PR description:

- **Summary** of changes
- **Testing** steps taken
- **Checklist**
  - [ ] Code follows style guidelines
  - [ ] Tests pass locally
  - [ ] Documentation updated (if applicable)

Thank you for contributing!
