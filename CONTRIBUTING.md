# Contributing to Fundalyze

Thank you for helping to improve Fundalyze! This document explains how to set up a development environment, follow the style rules and submit pull requests.

## Getting Started

1. **Fork** the repository on GitHub and clone your fork:
   ```bash
   git clone https://github.com/<your-user>/Fundalyze.git
   cd Fundalyze
   ```
2. **Create a Python virtual environment** using the helper scripts or manually:
   ```bash
   ./bootstrap_env.sh      # macOS / Linux
   ./bootstrap_env.ps1     # Windows PowerShell
   ```
   Both scripts create `.venv` and install dependencies from `requirements.txt`.
   Manual setup works as well:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   If JavaScript tooling is introduced, install Node.js and run `npm install` inside the appropriate folder.

3. **Configure environment variables** by copying `config/.env` from the example and adding your API keys.

## Code Style

- **Python** – follow [PEP 8](https://peps.python.org/pep-0008/). Format code with `black` and sort imports with `isort` before committing.
- **JavaScript** – use `prettier` and `eslint` if present.

## Running Tests

Execute the entire test suite with:
```bash
pytest -q
```
All tests must pass before you open a pull request. The suite should complete quickly; investigate and fix any failures.

## Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make your changes and commit with a short, present‑tense message.
3. Push the branch to your fork and open a pull request against `main`.

### Pull Request Template
Include the following in your PR description:

- **Summary** – what was changed and why
- **Testing** – commands run and their output
- **Checklist**
  - [ ] Code follows style guidelines
  - [ ] Tests pass locally
  - [ ] Documentation updated if needed

Example:

```markdown
### Summary
Adds new analytics module for RSI calculations.

### Testing
```
pytest -q
```

### Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated if needed
```

We appreciate your contributions!
