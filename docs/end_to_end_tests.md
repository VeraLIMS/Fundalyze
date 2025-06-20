# End-to-End Test Scenarios

This document outlines the automated end-to-end tests for Fundalyze.

## Report Generation Workflow

1. **Fetch and Compile** – For a given ticker the system fetches profile
   information, price history and financial statements. The test mocks the
   OpenBB API responses and verifies that `fetch_and_compile()` writes the
   expected CSV files and metadata in a temporary output folder.
2. **Dashboard Creation** – Using the generated CSV files the test invokes
   `create_dashboard()` which assembles a summary JSON report. The file is
   inspected to ensure the expected keys (e.g. `profile`, `history`) exist.

## Portfolio Manager Workflow

1. **Interactive CLI** – The test drives the `portfolio_manager` CLI by
   supplying a sequence of user inputs. It adds a ticker and then exits.
2. **Persistence** – After the CLI terminates, the in-memory portfolio is
   validated to contain the added ticker and that the Directus collection was
   updated.

These tests exercise the main user journeys without relying on network access
and run automatically as part of the test suite.

## Running the Tests

1. Install dependencies with `pip install -r requirements.txt`.
2. Run all tests using:
   ```bash
   pytest -q
   ```
3. Use `pytest -k <pattern> -s` to execute a subset while inspecting output.
