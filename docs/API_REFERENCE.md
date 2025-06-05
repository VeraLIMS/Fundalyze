# API Reference
This reference was generated with `pydoc`.

Help on package modules.analytics in modules:

NAME
    modules.analytics - Simple portfolio and group analysis utilities.

PACKAGE CONTENTS


FUNCTIONS
    correlation_matrix(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return Pearson correlation matrix for numeric columns.
    
    moving_average(series: 'pd.Series', window: 'int') -> 'pd.Series'
        Return rolling mean over ``window`` periods.
    
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
            When ``True`` print a progress line for each ticker.
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


Help on module modules.generate_report.report_generator in modules.generate_report:

NAME
    modules.generate_report.report_generator - script: report_generator.py

DESCRIPTION
    Dependencies:
        pip install openbb[all] matplotlib pandas
    
    Usage:
        python src/report_generator.py AAPL MSFT GOOGL

FUNCTIONS
    fetch_and_compile(symbol: 'str', base_output: 'str | None' = None, *, price_period: 'str' = '1mo', statements: 'list[str] | None' = None) -> 'None'
        Generate all report files for ``symbol``.
        
        Parameters
        ----------
        symbol:
            Ticker to process.
        base_output:
            Folder where ticker subdirectory will be created. Defaults to
            :func:`modules.config_utils.get_output_dir`.
        price_period:
            Price history duration passed to OpenBB/yfinance.
        statements:
            Iterable of statement types (``"income"``, ``"balance"``, ``"cash"``)
            to download. By default all three are fetched.

DATA
    obb = None

FILE
    /workspace/Fundalyze/modules/generate_report/report_generator.py


Help on module modules.interface in modules:

NAME
    modules.interface

FUNCTIONS
    print_header(title: 'str') -> 'None'
        Display a section heading consistently across menus.
    
    print_invalid_choice() -> 'None'
        Standard message for invalid menu selections.
    
    print_table(df: 'pd.DataFrame', *, showindex: 'bool' = False) -> 'None'
        Pretty-print a DataFrame using :mod:`tabulate`.

DATA
    INVALID_CHOICE_MSG = "Invalid choice. Enter a number from the menu or ...

FILE
    /workspace/Fundalyze/modules/interface.py



