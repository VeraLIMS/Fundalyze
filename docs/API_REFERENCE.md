# API Reference
This reference was generated with `pydoc`.

Help on package modules.analytics in modules

NNAAMMEE
    modules.analytics - Simple portfolio and group analysis utilities.

PPAACCKKAAGGEE  CCOONNTTEENNTTSS


FFUUNNCCTTIIOONNSS
    ccoorrrreellaattiioonn__mmaattrriixx(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return Pearson correlation matrix for numeric columns.
    
    mmoovviinngg__aavveerraaggee(series: 'pd.Series', window: 'int') -> 'pd.Series'
        Return rolling mean over ``window`` periods.
    
    ppeerrcceennttaaggee__cchhaannggee(series: 'pd.Series', periods: 'int' = 1) -> 'pd.Series'
        Return percent change from ``periods`` prior values.
    
    ppoorrttffoolliioo__ssuummmmaarryy(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return basic summary statistics for numeric columns.
    
    sseeccttoorr__ccoouunnttss(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return count of tickers per sector.

DDAATTAA
    ____aallll____ = ['portfolio_summary', 'sector_counts', 'correlation_matrix',...

FFIILLEE
    /workspace/Fundalyze/modules/analytics/__init__.py


Help on module modules.utils.math_utils in modules.utils

NNAAMMEE
    modules.utils.math_utils

FFUUNNCCTTIIOONNSS
    mmoovviinngg__aavveerraaggee(series: 'pd.Series', window: 'int') -> 'pd.Series'
        Return rolling mean over ``window`` periods.
    
    ppeerrcceennttaaggee__cchhaannggee(series: 'pd.Series', periods: 'int' = 1) -> 'pd.Series'
        Return percent change from ``periods`` prior values.

FFIILLEE
    /workspace/Fundalyze/modules/utils/math_utils.py


Help on module modules.data.fetching in modules.data

NNAAMMEE
    modules.data.fetching - Utility functions for retrieving financial data.

FFUUNNCCTTIIOONNSS
    ffeettcchh__bbaassiicc__ssttoocckk__ddaattaa(ticker: 'str', *, fallback: 'bool' = True, provider: 'str' = 'auto') -> 'dict'
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
    
    ffeettcchh__bbaassiicc__ssttoocckk__ddaattaa__bbaattcchh(tickers: 'list[str] | tuple[str, ...]', *, fallback: 'bool' = True, provider: 'str' = 'auto', dedup: 'bool' = False, progress: 'bool' = False, max_workers: 'int | None' = None) -> 'pd.DataFrame'
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

DDAATTAA
    BBAASSIICC__FFIIEELLDDSS = ['Ticker', 'Name', 'Sector', 'Industry', 'Current Price...
    FFMMPP__PPRROOFFIILLEE__UURRLL = 'https://financialmodelingprep.com/api/v3/profile/{s...

FFIILLEE
    /workspace/Fundalyze/modules/data/fetching.py


Help on module modules.generate_report.report_generator in modules.generate_report

NNAAMMEE
    modules.generate_report.report_generator - script: report_generator.py

DDEESSCCRRIIPPTTIIOONN
    Dependencies:
        pip install openbb[all] matplotlib pandas
    
    Usage:
        python src/report_generator.py AAPL MSFT GOOGL

FFUUNNCCTTIIOONNSS
    ffeettcchh__aanndd__ccoommppiillee(symbol: 'str', base_output: 'str | None' = None, *, price_period: 'str' = '1mo', statements: 'list[str] | None' = None) -> 'None'
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

DDAATTAA
    oobbbb = None

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/report_generator.py


Help on module modules.interface in modules

NNAAMMEE
    modules.interface

FFUUNNCCTTIIOONNSS
    pprriinntt__hheeaaddeerr(title: 'str') -> 'None'
        Display a section heading consistently across menus.
    
    pprriinntt__iinnvvaalliidd__cchhooiiccee() -> 'None'
        Standard message for invalid menu selections.
    
    pprriinntt__ttaabbllee(df: 'pd.DataFrame', *, showindex: 'bool' = False) -> 'None'
        Pretty-print a DataFrame using :mod:`tabulate`.

DDAATTAA
    IINNVVAALLIIDD__CCHHOOIICCEE__MMSSGG = "Invalid choice. Enter a number from the menu or ...

FFIILLEE
    /workspace/Fundalyze/modules/interface.py


