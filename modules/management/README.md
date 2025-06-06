# modules.management

Command line utilities for interacting with portfolio data stored in Directus.
The portfolio manager and group analysis tools read and write directly to
Directus collections, relying on `modules.data.unified_fetcher` to pull
company information.

Run `python scripts/main.py portfolio` to manage your holdings or use the
`--no-openbb` flag to disable OpenBB during data fetches.
