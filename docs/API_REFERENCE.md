# API Reference

This reference is automatically generated using
[pdoc](https://pdoc.dev). To update the documentation run:

```bash
pdoc --output-dir docs --force modules
```

## modules.analytics
```
Python Library Documentation: package modules.analytics in modules

NAME
    modules.analytics - Simple portfolio and group analysis utilities.

PACKAGE CONTENTS


FUNCTIONS
    correlation_matrix(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return Pearson correlation matrix for numeric columns.
    
    moving_average(series: 'pd.Series', window: 'int') -> 'pd.Series'
        Return rolling mean over ``window`` periods.
    
    percentage_change(series: 'pd.Series', periods: 'int' = 1) -> 'pd.Series'
        Return percent change from ``periods`` prior values.
    
    portfolio_summary(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return basic summary statistics for numeric columns.
    
    sector_counts(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return count of tickers per sector.

DATA
    __all__ = ['portfolio_summary', 'sector_counts', 'correlation_matrix',...

FILE
    /workspace/Fundalyze/modules/analytics/__init__.py


```


## modules.management.portfolio_manager.portfolio_manager
```
Python Library Documentation: module modules.management.portfolio_manager.portfolio_manager in modules.management.portfolio_manager

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
    
    ticker_exists(df: pandas.core.frame.DataFrame, tk: str) -> bool
        Return True if the ticker already exists in the portfolio.
    
    update_tickers(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Refresh data for each ticker via yfinance.
    
    view_portfolio(portfolio: pandas.core.frame.DataFrame)
        Display the current portfolio in a tabular format.

DATA
    COLUMNS = ['Ticker', 'Name', 'Sector', 'Industry', 'Current Price', 'M...
    C_DIRECTUS_COLLECTION = 'portfolio'
    FROM_DIRECTUS = {'company_name': 'Name', 'current_price': 'Current Pri...
    PORTFOLIO_FILE = 'portfolio.xlsx'
    USE_DIRECTUS = False

FILE
    /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py


```

## modules.management.group_analysis
```
Python Library Documentation: package modules.management.group_analysis in modules.management

NAME
    modules.management.group_analysis

PACKAGE CONTENTS
    group_analysis

FILE
    /workspace/Fundalyze/modules/management/group_analysis/__init__.py


```

## modules.management.note_manager
```
Python Library Documentation: package modules.management.note_manager in modules.management

NAME
    modules.management.note_manager

PACKAGE CONTENTS
    note_manager

FUNCTIONS
    create_note(title: str, content: str = '') -> pathlib.Path
        Create a new note with the given title and content.
    
    get_note_path(title: str) -> pathlib.Path
        Return the Path for a given note title.
    
    list_notes() -> List[str]
        Return a list of available note titles (slugs).
    
    parse_links(content: str) -> List[str]
        Return a list of note titles referenced via [[wikilink]] syntax.
    
    read_note(title: str) -> Optional[str]
        Return the contents of a note, or None if it doesn't exist.
    
    run_note_manager() -> None
        Interactive menu for creating and viewing notes.
    
    slugify(title: str) -> str
        Convert a note title into a filesystem-friendly slug.

DATA
    __all__ = ['create_note', 'get_note_path', 'list_notes', 'parse_links'...

FILE
    /workspace/Fundalyze/modules/management/note_manager/__init__.py


```

## modules.data.fetching
```
Python Library Documentation: module modules.data.fetching in modules.data

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
    
    fetch_basic_stock_data_batch(tickers: 'list[str] | tuple[str, ...]', *, fallback: 'bool' = True, provider: 'str' = 'auto', dedup: 'bool' = False, progress: 'bool' = False, max_workers: 'int | None' = None) -> 'pd.DataFrame'
        Fetch :func:`fetch_basic_stock_data` for multiple tickers.
        
        Parameters
        ----------
        tickers:
            Iterable of ticker symbols.
        fallback:
            Passed through to :func:`fetch_basic_stock_data`.
        provider:
            Data source to use: ``"auto"`` (default), ``"yf"`` or ``"fmp"``.
        
        dedup:
            If ``True``, remove duplicate symbols before fetching.
        progress:
            When ``True`` display a progress bar while fetching. The bar works for
            both sequential and parallel execution.
        max_workers:
            If greater than 1, fetch tickers in parallel using ``ThreadPoolExecutor``.
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with one row per ticker and columns defined in
            :data:`BASIC_FIELDS`.

DATA
    BASIC_FIELDS = ['Ticker', 'Name', 'Sector', 'Industry', 'Current Price...
    FMP_PROFILE_URL = 'https://financialmodelingprep.com/api/v3/profile/{s...

FILE
    /workspace/Fundalyze/modules/data/fetching.py


```

## modules.utils.data_utils
```
Python Library Documentation: module modules.utils.data_utils in modules.utils

NAME
    modules.utils.data_utils - Utility helpers for pandas data processing.

FUNCTIONS
    ensure_period_column(df: 'pd.DataFrame', column_name: 'str' = 'Period') -> 'pd.DataFrame'
        Ensure ``df`` has a period column by resetting index if needed.
    
    read_csv_if_exists(path: 'Path', **kwargs) -> 'Optional[pd.DataFrame]'
        Return DataFrame from ``path`` if the file exists else ``None``.
    
    read_json_if_exists(path: 'Path') -> 'Optional[Any]'
        Return deserialized JSON object from ``path`` if it exists.
    
    strip_timezones(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return copy of ``df`` with timezone information removed.

DATA
    Optional = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FILE
    /workspace/Fundalyze/modules/utils/data_utils.py


```

