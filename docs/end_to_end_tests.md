# End-to-End Test Scenarios

This document outlines the automated end-to-end tests for Fundalyze.

## Report Generation Workflow

1. **Fetch and Compile** – For a given ticker the system fetches profile
   information, price history and financial statements. The test mocks the
   OpenBB API responses and verifies that `fetch_and_compile()` writes the
   expected CSV files and metadata in a temporary output folder.
2. **Dashboard Creation** – Using the generated CSV files the test invokes
   `create_dashboard()` which combines the data into an Excel workbook. The
   workbook is inspected to ensure the basic sheets (e.g. `Profile`,
   `PriceHistory`) exist.

## Portfolio Manager Workflow

1. **Interactive CLI** – The test drives the `portfolio_manager` CLI by
   supplying a sequence of user inputs. It adds a ticker and then exits.
2. **Persistence** – After the CLI terminates, the portfolio Excel file in the
   temporary directory is read and validated to contain the added ticker.

These tests exercise the main user journeys without relying on network access
and run automatically as part of the test suite.
