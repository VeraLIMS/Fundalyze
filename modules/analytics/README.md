# modules.analytics

Small helper functions for quick DataFrame analysis. These utilities are
used by the CLI tools to summarize portfolio data stored in Directus.

Available functions:
- `portfolio_summary(df)` – mean/min/max stats for numeric columns
- `sector_counts(df)` – frequency of tickers by sector
- `correlation_matrix(df)` – correlation matrix for numeric data
- `missing_field_counts(df)` – count of missing values per column
