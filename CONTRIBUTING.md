# Contributing to Fundalyze

Thank you for considering a contribution! This guide shows how to set up a local development environment, follow the style guidelines and submit pull requests.

## Getting Started

1. **Fork** the repository on GitHub then clone your fork:
   ```bash
   git clone https://github.com/<your-user>/Fundalyze.git
   cd Fundalyze
   ```
2. **Set up a virtual environment** using the helper scripts or manually:
   ```bash
   ./bootstrap_env.sh      # macOS / Linux
   ./bootstrap_env.ps1     # Windows PowerShell
   ```
   Both scripts create `.venv` and install dependencies from `requirements.txt`.
   Manual setup works too:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   If JavaScript tooling is used, install Node.js and run `npm install` in the
   relevant directory.
3. **Configure environment variables**. Copy the example `.env` and add your API
 keys as described in [docs/configuration.md](docs/configuration.md).

### Repository Layout

The codebase is organized into a few top-level packages:

```
modules/analytics      # DataFrame analysis helpers
modules/data           # Data fetching and Directus utilities
modules/management     # CLI tools
modules/utils          # Shared helper functions
scripts/               # Entry points (main menu, helpers)
tests/                 # Pytest suite
```
All persistent data is stored in Directus collections.

## Code Style

- **Python** – follow [PEP 8](https://peps.python.org/pep-0008/) and format with
  `black`; sort imports using `isort`.
- **JavaScript** – run `prettier` and `eslint` if the project contains JS files.

## Running Tests

Execute the suite before committing:
```bash
pytest -q
npm test  # if applicable
```
All tests must pass. Investigate and fix any failures.

## Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-change
   ```
2. Make your changes and commit with a short, present‑tense message.
3. Push the branch to your fork and open a pull request against `main`.

### Pull Request Template
Include the following in your PR description:

```markdown
### Summary
Describe the change.

### Testing
```bash
pytest -q
```
Include any other relevant commands.

### Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated if needed
```

We appreciate your contributions!
