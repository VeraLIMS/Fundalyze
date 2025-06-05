Help on package modules.analytics in modules:

NAME
    modules.analytics - Simple portfolio and group analysis utilities.

PACKAGE CONTENTS


FUNCTIONS
    correlation_matrix(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return Pearson correlation matrix for numeric columns.
    
    portfolio_summary(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return basic summary statistics for numeric columns.
    
    sector_counts(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return count of tickers per sector.

FILE
    /workspace/Fundalyze/modules/analytics/__init__.py


Help on module modules.data.fetching in modules.data:

NAME
    modules.data.fetching - Utility functions for retrieving financial data.

FUNCTIONS
    fetch_basic_stock_data(ticker: 'str', *, fallback: 'bool' = True, provider: 'str' = 'auto') -> 'dict'
        Fetch key fundamental data for a ticker.
        
        Parameters
        ----------
        ticker:
            Stock symbol to fetch.
        fallback:
            When ``provider='auto'`` and yfinance returns incomplete data,
            query FMP as a secondary source.
        provider:
            ``'yf'`` to use yfinance only, ``'fmp'`` for FMP only,
            or ``'auto'`` (default) to try yfinance then FMP if ``fallback``.

DATA
    BASIC_FIELDS = ['Ticker', 'Name', 'Sector', 'Industry', 'Current Price...
    FMP_PROFILE_URL = 'https://financialmodelingprep.com/api/v3/profile/{s...

FILE
    /workspace/Fundalyze/modules/data/fetching.py


Help on module modules.generate_report.report_generator in modules.generate_report:

NAME
    modules.generate_report.report_generator - script: report_generator.py

DESCRIPTION
    Dependencies:
        pip install openbb[all] matplotlib pandas
    
    Usage:
        python src/report_generator.py AAPL MSFT GOOGL

FUNCTIONS
    fetch_and_compile(symbol: str, base_output: str | None = None)
        1) Create output/<symbol>/
        2) Fetch company profile, save as profile.csv, record source & source_url
        3) Fetch 1mo prices, save 1mo_prices.csv & 1mo_close.png, record sources/URLs
        4) Fetch income/balance/cash (annual & quarterly), save CSVs, record sources/URLs
        5) Write report.md with clickable [label](url) for each source
        6) Write metadata.json containing {"source", "source_url", "fetched_at"} for each file

DATA
    obb = None

FILE
    /workspace/Fundalyze/modules/generate_report/report_generator.py


Help on module modules.generate_report.excel_dashboard in modules.generate_report:

NAME
    modules.generate_report.excel_dashboard - # src/generate_report/excel_dashboard.py

FUNCTIONS
    create_and_open_dashboard(output_root: str | None = None, *, tickers: Optional[Iterable[str]] = None)
        Create an Excel dashboard (with named Tables) and open it automatically.
    
    create_dashboard(output_root: str | None = None, *, tickers: Optional[Iterable[str]] = None) -> pathlib.Path
        1) Find subfolders under output_root (one per ticker).
        2) Read these CSVs if present:
             - profile.csv
             - 1mo_prices.csv
             - income_annual.csv
             - income_quarter.csv
             - balance_annual.csv
             - balance_quarter.csv
             - cash_annual.csv
             - cash_quarter.csv
        
        3) Build two “normal” DataFrames:
             df_profiles = _safe_concat_normal(profiles)
             df_prices   = _safe_concat_normal(prices)
        
           And six “transposed” DataFrames (with stringified period headers):
             df_inc_ann  = _transpose_financials(income_ann)
             df_inc_qtr  = _transpose_financials(income_qtr)
             df_bal_ann  = _transpose_financials(balance_ann)
             df_bal_qtr  = _transpose_financials(balance_qtr)
             df_cash_ann = _transpose_financials(cash_ann)
             df_cash_qtr = _transpose_financials(cash_qtr)
        
        4) Write all eight DataFrames to:
             output_root/dashboard_<TIMESTAMP>.xlsx
           Converting each sheet into an Excel Table (so you can use structured references
           like `[Revenue]` or `[2022-12]` in formulas).
        
        Returns:
            Path to the newly created .xlsx file.
    
    show_dashboard_in_excel(dashboard_path: pathlib.Path)
        Open the newly created Excel file in the OS default application.

DATA
    Iterable = typing.Iterable
        A generic version of collections.abc.Iterable.
    
    Optional = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FILE
    /workspace/Fundalyze/modules/generate_report/excel_dashboard.py


Help on module modules.management.portfolio_manager.portfolio_manager in modules.management.portfolio_manager:

NAME
    modules.management.portfolio_manager.portfolio_manager - script: portfolio_manager.py

DESCRIPTION
    Dependencies:
        pip install yfinance pandas openpyxl
    
    Usage:
        python portfolio_manager.py
    
    Description:
        A simple CLI tool to manage a stock portfolio. You can:
        - Add tickers (automatically fetch key data via yfinance; if fetch fails, confirm/adjust ticker or enter data manually).
        - Remove tickers.
        - View current portfolio.
        - Data is persisted in an Excel file ("portfolio.xlsx") in the same directory.

FUNCTIONS
    add_tickers(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt the user to enter one or more tickers to add. For each ticker:
        - Attempt to fetch data via yfinance.
        - If fetch fails or missing, confirm/adjust ticker or allow manual fill.
        - Append a new row to the portfolio DataFrame.
    
    confirm_or_adjust_ticker(original: str) -> str
        If yfinance fetch fails, ask the user: "Is this the correct ticker?"
        If yes, return the same string. If no, prompt for a new ticker and return it.
    
    fetch_from_yfinance(ticker: str) -> dict
        Wrapper around :func:`modules.data.fetching.fetch_basic_stock_data`.
    
    load_portfolio(filepath: str) -> pandas.core.frame.DataFrame
        Load the portfolio either from Directus (if configured) or from a local
        Excel file. If loading fails, an empty DataFrame with the expected columns
        is returned.
    
    main()
    
    prompt_manual_entry(ticker: str) -> dict
        Prompt the user to manually fill out each field for a given ticker.
        Returns a dict mapping column names to user-provided values.
    
    remove_ticker(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt the user for a ticker to remove from the portfolio.
    
    save_portfolio(df: pandas.core.frame.DataFrame, filepath: str)
        Save the portfolio either to Directus (if configured) or to a local Excel
        file as fallback.
    
    update_tickers(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Refresh data for each ticker via yfinance.
    
    view_portfolio(portfolio: pandas.core.frame.DataFrame)
        Display the current portfolio in a tabular format.

DATA
    COLUMNS = ['Ticker', 'Name', 'Sector', 'Industry', 'Current Price', 'M...
    C_DIRECTUS_COLLECTION = 'portfolio'
    PORTFOLIO_FILE = 'portfolio.xlsx'
    USE_DIRECTUS = False

FILE
    /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py


Help on module modules.management.group_analysis.group_analysis in modules.management.group_analysis:

NAME
    modules.management.group_analysis.group_analysis - script: group_analysis.py

DESCRIPTION
    Dependencies:
        pip install yfinance pandas openpyxl
    
    Usage:
        python src/group_analysis.py
    
    Description:
        CLI tool to manage “groups” of stocks—e.g., those in the same sector or
        similar to a given portfolio holding. You can:
          - View existing groups and their members
          - Create a new group (optionally tied to a portfolio ticker)
          - Add tickers to a group (fetching key data via yfinance; manual override if necessary)
          - Remove tickers from a group
          - Delete an entire group
          - Link a group to a stock in your existing portfolio.xlsx
    
        Data is persisted in "groups.xlsx" alongside your portfolio.xlsx to allow
        later cross‐company comparison.

FUNCTIONS
    add_tickers_to_group(groups: pandas.core.frame.DataFrame, group_name: str) -> pandas.core.frame.DataFrame
        Prompt for tickers to add to a specific group. Fetch data, allow override.
        Append to 'groups' DataFrame under the given group_name.
    
    choose_group(portfolio: pandas.core.frame.DataFrame) -> str
        Ask user whether to link a new group to a portfolio ticker or create a custom name.
    
    confirm_or_adjust_ticker(original: str) -> str
        If yfinance fetch fails, ask: “Is this ticker correct?” If no, prompt new ticker.
        Return empty string to cancel.
    
    delete_group(groups: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt for a group to delete entirely (all its tickers).
    
    fetch_from_yfinance(ticker: str) -> dict
        Wrapper around :func:`modules.data.fetching.fetch_basic_stock_data`.
    
    load_groups(filepath: str) -> pandas.core.frame.DataFrame
        Load existing groups either from Directus or from Excel. If neither source
        is available, return an empty DataFrame with the expected columns.
    
    load_portfolio(filepath: str) -> pandas.core.frame.DataFrame
        Load the user’s portfolio from Excel. If missing, return empty DataFrame.
    
    main()
    
    prompt_manual_entry(ticker: str) -> dict
        If automated fetch fails or user overrides, prompt manual entry.
    
    remove_ticker_from_group(groups: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt for group and ticker to remove.
    
    save_groups(df: pandas.core.frame.DataFrame, filepath: str)
        Persist groups DataFrame either to Directus or to Excel as fallback.
    
    view_groups(groups: pandas.core.frame.DataFrame)
        Display all groups and their members in a readable format.

DATA
    COLUMNS = ['Group', 'Ticker', 'Name', 'Sector', 'Industry', 'Current P...
    GROUPS_COLLECTION = 'groups'
    GROUPS_FILE = 'groups.xlsx'
    PORTFOLIO_FILE = 'portfolio.xlsx'
    SETTINGS = {}
    USE_DIRECTUS = False

FILE
    /workspace/Fundalyze/modules/management/group_analysis/group_analysis.py


Help on module modules.config_utils in modules:

NAME
    modules.config_utils - Utilities for loading environment variables and user settings.

FUNCTIONS
    add_fmp_api_key(url: 'str') -> 'str'
        Append the FMP API key as a query parameter if configured.
    
    get_output_dir() -> 'Path'
        Return output directory path from ``OUTPUT_DIR`` env variable.
    
    load_env() -> 'Dict[str, str]'
        Return key-value pairs loaded from ``config/.env`` if it exists.
    
    load_settings() -> 'Dict[str, Any]'
        Return settings dictionary loaded from config/settings.json if it exists.
    
    save_env(env: 'Dict[str, str]') -> 'None'
        Write key-value pairs to ``config/.env``.
    
    save_settings(data: 'Dict[str, Any]') -> 'None'
        Persist the provided settings dictionary to ``config/settings.json``.

DATA
    CONFIG_DIR = PosixPath('/workspace/Fundalyze/config')
    Dict = typing.Dict
        A generic version of dict.
    
    ENV_PATH = PosixPath('/workspace/Fundalyze/config/.env')
    SETTINGS_PATH = PosixPath('/workspace/Fundalyze/config/settings.json')

FILE
    /workspace/Fundalyze/modules/config_utils.py


Help on module modules.utils.data_utils in modules.utils:

NAME
    modules.utils.data_utils - Utility helpers for pandas data processing.

FUNCTIONS
    ensure_period_column(df: 'pd.DataFrame', column_name: 'str' = 'Period') -> 'pd.DataFrame'
        Ensure ``df`` has a period column by resetting index if needed.
    
    read_csv_if_exists(path: 'Path', **kwargs) -> 'Optional[pd.DataFrame]'
        Return DataFrame from ``path`` if the file exists else ``None``.
    
    strip_timezones(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return copy of ``df`` with timezone information removed.

DATA
    Optional = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FILE
    /workspace/Fundalyze/modules/utils/data_utils.py


Help on module modules.interface in modules:

NAME
    modules.interface

FUNCTIONS
    print_invalid_choice() -> 'None'
        Standard message for invalid menu selections.
    
    print_table(df: 'pd.DataFrame', *, showindex: 'bool' = False) -> 'None'
        Pretty-print a DataFrame using :mod:`tabulate`.

DATA
    INVALID_CHOICE_MSG = 'Invalid choice. Please select a valid option.\n'

FILE
    /workspace/Fundalyze/modules/interface.py


