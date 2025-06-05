# Contributing to Fundalyze

Thanks for taking the time to contribute! This guide explains how to set up a development environment and the workflow for submitting changes.

## Getting Started

1. **Fork** the repository and clone your fork:
   ```bash
   git clone https://github.com/<your-user>/Fundalyze.git
   cd Fundalyze
   ```
2. **Create a Python virtual environment** using the helper scripts or manually:
   ```bash
   ./bootstrap_env.sh      # macOS/Linux
   ./bootstrap_env.ps1     # Windows PowerShell
   ```
   These scripts create `.venv` and install dependencies from `requirements.txt`.
   Manual setup is also fine:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   If you add any JavaScript tooling, install Node.js and run `npm install` in the appropriate directory.

## Code Style

- **Python** – follow [PEP 8](https://peps.python.org/pep-0008/). Format code with `black` and sort imports with `isort` before committing.
- **JavaScript** – use `prettier` and `eslint` if applicable.

## Running Tests

Execute the full suite with:
```bash
pytest -q
```
All tests must pass before sending a pull request. Additional helper scripts live under `scripts/` if you want to run tests individually.

## Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-change
   ```
2. Commit with a clear message describing *why* the change is needed.
3. Push your branch and open a pull request against `main`.

### Pull Request Template
Include the following in the PR description:

- **Summary** of changes
- **Testing** steps performed
- **Checklist**
  - [ ] Code follows style guidelines
  - [ ] Tests pass locally
  - [ ] Documentation updated if needed

We appreciate your help improving Fundalyze!
