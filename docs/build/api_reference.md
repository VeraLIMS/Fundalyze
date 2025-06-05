## modules.analytics
```
Python Library Documentation: package modules.analytics in modules

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


```

## modules.generate_report.report_generator
```
Python Library Documentation: module modules.generate_report.report_generator in modules.generate_report

NNAAMMEE
    modules.generate_report.report_generator - script: report_generator.py

DDEESSCCRRIIPPTTIIOONN
    Dependencies:
        pip install openbb[all] matplotlib pandas
    
    Usage:
        python src/report_generator.py AAPL MSFT GOOGL

FFUUNNCCTTIIOONNSS
    ffeettcchh__aanndd__ccoommppiillee(symbol: 'str', base_output: 'str | None' = None, *, price_period: 'str' = '1mo', statements: 'list[str] | None' = None, local_output: 'bool | None' = None, write_json: 'bool' = False) -> 'None'
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
        write_json:
            When ``True`` also output JSON files in addition to CSV/PNG.

DDAATTAA
    oobbbb = None

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/report_generator.py


```

## modules.generate_report.metadata_checker
```
Python Library Documentation: module modules.generate_report.metadata_checker in modules.generate_report

NNAAMMEE
    modules.generate_report.metadata_checker

DDEESSCCRRIIPPTTIIOONN
    This script examines each metadata.json under output/<TICKER>/,
    finds any files whose 'source' field indicates an ERROR, and
    re-fetches that piece of data via yfinance (or via FMP as a fallback
    for financial statements). It then overwrites the CSV and updates
    metadata.json with new source, source_url, and fetched_at timestamp.

FFUUNNCCTTIIOONNSS
    eennrriicchh__ttiicckkeerr__ffoollddeerr(ticker_dir: pathlib.Path)
        Examine metadata.json in ticker_dir, find any file entries whose 'source'
        starts with 'ERROR', and re-fetch them via yfinance (or FMP fallback).
        Overwrite the corresponding CSV, then update metadata.json accordingly.
    
    ffeettcchh__11mmoo__pprriicceess__yyff(symbol: str) -> pandas.core.frame.DataFrame
        Fetch 1‐month price history via yfinance (history). Returns a DataFrame
        with Date, Open, High, Low, Close, Adj Close, Volume.
    
    ffeettcchh__ffiinn__ssttmmtt__ffrroomm__yyff(symbol: str, stmt_key: str) -> pandas.core.frame.DataFrame
        Given symbol and a yfinance attribute name (e.g. 'financials', 'quarterly_financials',
        'balance_sheet', etc.), attempt to pull that DataFrame. Returns empty DataFrame
        if nothing is returned. The caller will decide if fallback to FMP is needed.
    
    ffeettcchh__ffmmpp__ssttaatteemmeenntt(symbol: str, stmt_endpoint: str, period: str) -> pandas.core.frame.DataFrame
        stmt_endpoint: 'income-statement', 'balance-sheet-statement', or 'cash-flow-statement'.
        period: 'annual' or 'quarter'
    
    ffeettcchh__pprrooffiillee__ffrroomm__yyff(symbol: str) -> pandas.core.frame.DataFrame
        Fetch company profile using yfinance: we construct a DataFrame
        with columns similar to profile.csv from report_generator.py.
    
    mmaaiinn(output_root: str | None = None)
    
    rruunn__ffoorr__ttiicckkeerrss(tickers, output_root: str | None = None)
        Run metadata enrichment only for the specified ticker list.

DDAATTAA
    FFMMPP__BBAASSEE = 'https://financialmodelingprep.com/api/v3'

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/metadata_checker.py


```

## modules.generate_report.fallback_data
```
Python Library Documentation: module modules.generate_report.fallback_data in modules.generate_report

NNAAMMEE
    modules.generate_report.fallback_data - fallback_data.py

DDEESSCCRRIIPPTTIIOONN
    When some CSV files (profile, price history, or financial statements) fail to fetch
    via the primary methods (OpenBB → yfinance → FMP), this module attempts a “full”
    yfinance-based fallback to repopulate all missing files for a given ticker.
    
    Usage:
        run_fallback_data()  # scans output/, attempts fix for each ticker folder

FFUUNNCCTTIIOONNSS
    eennrriicchh__ttiicckkeerr__ffoollddeerr(ticker_dir: pathlib.Path)
        1. Load metadata.json for this ticker.
        2. For each file with source.startswith("ERROR"), attempt a targeted re-fetch:
             - For profile.csv: try FMP->DataFrame
             - For 1mo_prices.csv: try yfinance.history
             - For <stmt>_annual.csv or _quarter.csv: try yfinance.<stmt> or fallback to FMP
        3. If any single-file fetch still fails, run yf_full_fetch(symbol) to recreate all CSVs.
        4. Update metadata.json with new 'source', 'source_url', and 'fetched_at'.
    
    ffeettcchh__11mmoo__pprriicceess__ffmmpp(symbol: str) -> pandas.core.frame.DataFrame
        Fetch 1-month daily price history from FMP.
    
    ffeettcchh__ffmmpp__ssttaatteemmeenntt(symbol: str, stmt_endpoint: str, period: str) -> pandas.core.frame.DataFrame
        Fetch financial statement from FMP. stmt_endpoint e.g. 'income-statement',
        'balance-sheet-statement', 'cash-flow-statement'. Period: 'annual' or 'quarter'.
        Returns a DataFrame indexed by date if successful; raises ValueError otherwise.
    
    ffeettcchh__pprrooffiillee__ffrroomm__ffmmpp(symbol: str) -> pandas.core.frame.DataFrame
        Fetch company profile from Financial Modeling Prep. Returns a DataFrame with
        at least these columns: symbol, longName, sector, industry, marketCap, website.
        Raises ValueError if no data is returned.
    
    rruunn__ffaallllbbaacckk__ddaattaa(tickers=None, output_root: str | None = None)
        Run fallback enrichment for all or selected tickers.
    
    yyff__ffuullll__ffeettcchh(symbol: str)
        A “full” fallback that uses yfinance to retrieve Profile, 1-month price history,
        and all four financial statements. Writes files into output/<symbol>/.

DDAATTAA
    FFMMPP__BBAASSEE = 'https://financialmodelingprep.com/api/v3'

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/fallback_data.py


```

## modules.generate_report.excel_dashboard
```
Python Library Documentation: module modules.generate_report.excel_dashboard in modules.generate_report

NNAAMMEE
    modules.generate_report.excel_dashboard - Create Excel dashboards from ticker report data.

FFUUNNCCTTIIOONNSS
    ccrreeaattee__aanndd__ooppeenn__ddaasshhbbooaarrdd(output_root: str | None = None, *, tickers: Optional[Iterable[str]] = None, progress: bool = False)
        Create an Excel dashboard (with named Tables) and open it automatically.
        
        Parameters
        ----------
        output_root:
            Base folder containing ticker subdirectories.
        tickers:
            Optional subset of tickers to include.
        progress:
            When ``True`` display a progress bar while loading CSV files.
    
    ccrreeaattee__ddaasshhbbooaarrdd(output_root: str | None = None, *, tickers: Optional[Iterable[str]] = None, progress: bool = False) -> pathlib.Path
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
        
        Parameters
        ----------
        output_root:
            Base folder containing ticker subdirectories.
        tickers:
            Optional subset of tickers to include. Defaults to all found in
            ``output_root``.
        progress:
            When ``True`` display a progress bar while loading CSV files.
        
        Returns:
            Path to the newly created .xlsx file.
    
    sshhooww__ddaasshhbbooaarrdd__iinn__eexxcceell(dashboard_path: pathlib.Path)
        Open the newly created Excel file in the OS default application.

DDAATTAA
    IItteerraabbllee = typing.Iterable
        A generic version of collections.abc.Iterable.
    
    OOppttiioonnaall = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/excel_dashboard.py


```

## modules.generate_report.yf_fallback
```
Python Library Documentation: module modules.generate_report.yf_fallback in modules.generate_report

NNAAMMEE
    modules.generate_report.yf_fallback - Fallback data retrieval using only yfinance.

FFUUNNCCTTIIOONNSS
    ffeettcchh__aanndd__ddiissppllaayy(symbol: str)
        1) Fetch basic company info and print selected fields.
        2) Download and print 1 month of price history.
        3) Fetch annual and quarterly financial statements and print/save them.
        This writes files into: <project_root>/output/<symbol>/

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/yf_fallback.py


```

## modules.generate_report.utils
```
Python Library Documentation: module modules.generate_report.utils in modules.generate_report

NNAAMMEE
    modules.generate_report.utils - Small helper utilities for report generation.

FFUUNNCCTTIIOONNSS
    iissoo__ttiimmeessttaammpp__uuttcc() -> 'str'
        Return current UTC timestamp in ISO 8601 format.

FFIILLEE
    /workspace/Fundalyze/modules/generate_report/utils.py


```

## modules.management.portfolio_manager.portfolio_manager
```
Python Library Documentation: module modules.management.portfolio_manager.portfolio_manager in modules.management.portfolio_manager

NNAAMMEE
    modules.management.portfolio_manager.portfolio_manager - script: portfolio_manager.py

DDEESSCCRRIIPPTTIIOONN
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

FFUUNNCCTTIIOONNSS
    aadddd__ttiicckkeerrss(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt the user to enter one or more tickers to add. For each ticker:
        - Attempt to fetch data via yfinance.
        - If fetch fails or missing, confirm/adjust ticker or allow manual fill.
        - Append a new row to the portfolio DataFrame.
    
    ccoonnffiirrmm__oorr__aaddjjuusstt__ttiicckkeerr(original: str) -> str
        If yfinance fetch fails, ask the user: "Is this the correct ticker?"
        If yes, return the same string. If no, prompt for a new ticker and return it.
    
    ffeettcchh__ffrroomm__yyffiinnaannccee(ticker: str) -> dict
        Wrapper around :func:`modules.data.fetching.fetch_basic_stock_data`.
    
    llooaadd__ppoorrttffoolliioo(filepath: str) -> pandas.core.frame.DataFrame
        Load the portfolio either from Directus (if configured) or from a local
        Excel file. If loading fails, an empty DataFrame with the expected columns
        is returned.
    
    mmaaiinn()
    
    pprroommpptt__mmaannuuaall__eennttrryy(ticker: str) -> dict
        Prompt the user to manually fill out each field for a given ticker.
        Returns a dict mapping column names to user-provided values.
    
    rreemmoovvee__ttiicckkeerr(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt the user for a ticker to remove from the portfolio.
    
    ssaavvee__ppoorrttffoolliioo(df: pandas.core.frame.DataFrame, filepath: str)
        Save the portfolio either to Directus (if configured) or to a local Excel
        file as fallback.
    
    ttiicckkeerr__eexxiissttss(df: pandas.core.frame.DataFrame, tk: str) -> bool
        Return True if the ticker already exists in the portfolio.
    
    uuppddaattee__ttiicckkeerrss(portfolio: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Refresh data for each ticker via yfinance.
    
    vviieeww__ppoorrttffoolliioo(portfolio: pandas.core.frame.DataFrame)
        Display the current portfolio in a tabular format.

DDAATTAA
    CCOOLLUUMMNNSS = ['Ticker', 'Name', 'Sector', 'Industry', 'Current Price', 'M...
    CC__DDIIRREECCTTUUSS__CCOOLLLLEECCTTIIOONN = 'portfolio'
    FFRROOMM__DDIIRREECCTTUUSS = {'company_name': 'Name', 'current_price': 'Current Pri...
    PPOORRTTFFOOLLIIOO__FFIILLEE = 'portfolio.xlsx'
    UUSSEE__DDIIRREECCTTUUSS = False

FFIILLEE
    /workspace/Fundalyze/modules/management/portfolio_manager/portfolio_manager.py


```

## modules.management.group_analysis.group_analysis
```
Python Library Documentation: module modules.management.group_analysis.group_analysis in modules.management.group_analysis

NNAAMMEE
    modules.management.group_analysis.group_analysis - script: group_analysis.py

DDEESSCCRRIIPPTTIIOONN
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

FFUUNNCCTTIIOONNSS
    aadddd__ttiicckkeerrss__ttoo__ggrroouupp(groups: pandas.core.frame.DataFrame, group_name: str) -> pandas.core.frame.DataFrame
        Prompt for tickers to add to a specific group. Fetch data, allow override.
        Append to 'groups' DataFrame under the given group_name.
    
    cchhoooossee__ggrroouupp(portfolio: pandas.core.frame.DataFrame) -> str
        Ask user whether to link a new group to a portfolio ticker or create a custom name.
    
    ccoonnffiirrmm__oorr__aaddjjuusstt__ttiicckkeerr(original: str) -> str
        If yfinance fetch fails, ask: “Is this ticker correct?” If no, prompt new ticker.
        Return empty string to cancel.
    
    ddeelleettee__ggrroouupp(groups: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt for a group to delete entirely (all its tickers).
    
    ffeettcchh__ffrroomm__yyffiinnaannccee(ticker: str) -> dict
        Wrapper around :func:`modules.data.fetching.fetch_basic_stock_data`.
    
    llooaadd__ggrroouuppss(filepath: str) -> pandas.core.frame.DataFrame
        Load existing groups either from Directus or from Excel. If neither source
        is available, return an empty DataFrame with the expected columns.
    
    llooaadd__ppoorrttffoolliioo(filepath: str) -> pandas.core.frame.DataFrame
        Load the user’s portfolio from Excel. If missing, return empty DataFrame.
    
    mmaaiinn()
    
    pprroommpptt__mmaannuuaall__eennttrryy(ticker: str) -> dict
        If automated fetch fails or user overrides, prompt manual entry.
    
    rreemmoovvee__ttiicckkeerr__ffrroomm__ggrroouupp(groups: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame
        Prompt for group and ticker to remove.
    
    ssaavvee__ggrroouuppss(df: pandas.core.frame.DataFrame, filepath: str)
        Persist groups DataFrame either to Directus or to Excel as fallback.
    
    vviieeww__ggrroouuppss(groups: pandas.core.frame.DataFrame)
        Display all groups and their members in a readable format.

DDAATTAA
    CCOOLLUUMMNNSS = ['Group', 'Ticker', 'Name', 'Sector', 'Industry', 'Current P...
    FFRROOMM__DDIIRREECCTTUUSS = {'company_name': 'Name', 'current_price': 'Current Pri...
    GGRROOUUPPSS__CCOOLLLLEECCTTIIOONN = 'groups'
    GGRROOUUPPSS__FFIILLEE = 'groups.xlsx'
    PPOORRTTFFOOLLIIOO__FFIILLEE = 'portfolio.xlsx'
    SSEETTTTIINNGGSS = {}
    UUSSEE__DDIIRREECCTTUUSS = True

FFIILLEE
    /workspace/Fundalyze/modules/management/group_analysis/group_analysis.py


```

## modules.management.note_manager.note_manager
```
Python Library Documentation: module modules.management.note_manager.note_manager in modules.management.note_manager

NNAAMMEE
    modules.management.note_manager.note_manager - Command line note manager with wiki-style links.

FFUUNNCCTTIIOONNSS
    ccrreeaattee__nnoottee(title: str, content: str = '') -> pathlib.Path
        Create a new note with the given title and content.
    
    ggeett__nnoottee__ppaatthh(title: str) -> pathlib.Path
        Return the Path for a given note title.
    
    ggeett__nnootteess__ddiirr() -> pathlib.Path
        Return the notes directory, creating it if needed.
    
    lliisstt__nnootteess() -> List[str]
        Return a list of available note titles (slugs).
    
    ppaarrssee__lliinnkkss(content: str) -> List[str]
        Return a list of note titles referenced via [[wikilink]] syntax.
    
    rreeaadd__nnoottee(title: str) -> Optional[str]
        Return the contents of a note, or None if it doesn't exist.
    
    rruunn__nnoottee__mmaannaaggeerr() -> None
        Interactive menu for creating and viewing notes.
    
    sslluuggiiffyy(title: str) -> str
        Convert a note title into a filesystem-friendly slug.

DDAATTAA
    LLiisstt = typing.List
        A generic version of list.
    
    OOppttiioonnaall = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FFIILLEE
    /workspace/Fundalyze/modules/management/note_manager/note_manager.py


```

## modules.management.directus_tools.directus_wizard
```
Python Library Documentation: module modules.management.directus_tools.directus_wizard in modules.management.directus_tools

NNAAMMEE
    modules.management.directus_tools.directus_wizard - Interactive wizard for configuring Directus integration.

FFUUNNCCTTIIOONNSS
    rruunn__ddiirreeccttuuss__wwiizzaarrdd() -> None
        Interactive wizard for common Directus API operations.

FFIILLEE
    /workspace/Fundalyze/modules/management/directus_tools/directus_wizard.py


```

## modules.management.settings_manager.settings_manager
```
Python Library Documentation: module modules.management.settings_manager.settings_manager in modules.management.settings_manager

NNAAMMEE
    modules.management.settings_manager.settings_manager - Interactive manager for `config/settings.json` and `.env`.

FFUUNNCCTTIIOONNSS
    rruunn__sseettttiinnggss__mmaannaaggeerr() -> 'None'
        Interactive menu to edit configuration and run setup wizards.

DDAATTAA
    CCOONNFFIIGG__DDIIRR = PosixPath('/workspace/Fundalyze/config')
    DDiicctt = typing.Dict
        A generic version of dict.

FFIILLEE
    /workspace/Fundalyze/modules/management/settings_manager/settings_manager.py


```

## modules.data.fetching
```
Python Library Documentation: module modules.data.fetching in modules.data

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
            When ``True`` display a progress bar while fetching. The bar works for
            both sequential and parallel execution.
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


```

## modules.data.directus_client
```
Python Library Documentation: module modules.data.directus_client in modules.data

NNAAMMEE
    modules.data.directus_client - Thin wrapper around the Directus REST API.

FFUUNNCCTTIIOONNSS
    cclleeaann__rreeccoorrdd(record: Dict[str, Any]) -> Dict[str, Any]
        Return a copy of ``record`` with NaN/inf values converted to ``None``.
    
    ccrreeaattee__ffiieelldd(collection: str, field: str, field_type: str = 'string', **kwargs)
        Create a new field in the given collection.
    
    ddeelleettee__iitteemm(collection: str, item_id: Any) -> bool
        Delete an item by ``item_id`` from ``collection``.
    
    ddiirreeccttuuss__rreeqquueesstt(method: str, path: str, **kwargs) -> Optional[Dict[str, Any]]
        Send a request to the Directus API and return the JSON response.
    
    ffeettcchh__iitteemmss(collection: str, limit: int | None = None) -> list[typing.Dict[str, typing.Any]]
        Fetch items from a Directus collection.
    
    ffeettcchh__iitteemmss__ffiilltteerreedd(collection: str, params: Dict[str, Any]) -> list[typing.Dict[str, typing.Any]]
        Fetch items from ``collection`` applying Directus filter parameters.
    
    iinnsseerrtt__iitteemmss(collection: str, items)
        Insert one or more items into a Directus collection.
    
    lliisstt__ccoolllleeccttiioonnss() -> list[str]
        Return available collection names.
    
    lliisstt__ffiieellddss(collection: str) -> list[str]
        Return list of field names for the given Directus collection.
    
    lliisstt__ffiieellddss__wwiitthh__ttyyppeess(collection: str) -> list[typing.Dict[str, typing.Any]]
        Return field metadata including name and type for a collection.
    
    rreellooaadd__eennvv() -> None
        Reload Directus environment variables from ``config/.env``.
    
    uuppddaattee__iitteemm(collection: str, item_id: Any, updates: Dict[str, Any])
        Update a single item by ``item_id`` in ``collection``.

DDAATTAA
    CCFF__AACCCCEESSSS__CCLLIIEENNTT__IIDD = None
    CCFF__AACCCCEESSSS__CCLLIIEENNTT__SSEECCRREETT = None
    DDIIRREECCTTUUSS__TTOOKKEENN = None
    DDIIRREECCTTUUSS__UURRLL = 'https://api.veralims.com'
    DDiicctt = typing.Dict
        A generic version of dict.
    
    llooggggeerr = <Logger modules.data.directus_client (WARNING)>

FFIILLEE
    /workspace/Fundalyze/modules/data/directus_client.py


```

## modules.data.directus_mapper
```
Python Library Documentation: module modules.data.directus_mapper in modules.data

NNAAMMEE
    modules.data.directus_mapper - Utilities for mapping DataFrame fields to Directus collections.

FFUUNNCCTTIIOONNSS
    eennssuurree__ffiieelldd__mmaappppiinngg(collection: str, df: 'pd.DataFrame') -> Dict[str, Any]
        Interactive mapping helper for DataFrame columns.
        
        For each column in ``df`` that is unmapped or mapped to a non-existent
        Directus field, prompt the user for the target field name. The mapping file
        is updated and returned.
    
    iinntteerraaccttiivvee__pprreeppaarree__rreeccoorrddss(collection: str, records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]
        Like :func:`prepare_records` but prompt for unmapped fields.
        
        Any newly mapped fields are saved back to ``directus_field_map.json``.
    
    llooaadd__ffiieelldd__mmaapp() -> Dict[str, Any]
        Return mapping dictionary loaded from ``config/directus_field_map.json``.
    
    pprreeppaarree__rreeccoorrddss(collection: str, records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]
        Rename and filter record fields for Directus insertion.
    
    rreeffrreesshh__ffiieelldd__mmaapp() -> Dict[str, Any]
        Update mapping with fields from Directus collections.
    
    ssaavvee__ffiieelldd__mmaapp(mapping: Dict[str, Any]) -> None
        Save mapping dictionary to ``config/directus_field_map.json``.

DDAATTAA
    DDiicctt = typing.Dict
        A generic version of dict.
    
    IItteerraabbllee = typing.Iterable
        A generic version of collections.abc.Iterable.
    
    LLiisstt = typing.List
        A generic version of list.
    
    MMAAPP__FFIILLEE = PosixPath('/workspace/Fundalyze/config/directus_field_map.j...
    PPRROOJJEECCTT__RROOOOTT = PosixPath('/workspace/Fundalyze')
    TTYYPPEE__CCHHEECCKKIINNGG = False
    llooggggeerr = <Logger modules.data.directus_mapper (WARNING)>

FFIILLEE
    /workspace/Fundalyze/modules/data/directus_mapper.py


```

## modules.data.term_mapper
```
Python Library Documentation: module modules.data.term_mapper in modules.data

NNAAMMEE
    modules.data.term_mapper - Maintain mapping of search terms to API field names.

FFUUNNCCTTIIOONNSS
    aadddd__aalliiaass(canonical: str, alias: str)
    
    llooaadd__mmaappppiinngg() -> Dict[str, List[str]]
    
    rreessoollvvee__tteerrmm(term: str) -> str
        Return canonical term for given term. If unknown, ask user.
    
    ssaavvee__mmaappppiinngg(mapping: Dict[str, List[str]])

DDAATTAA
    DDiicctt = typing.Dict
        A generic version of dict.
    
    LLiisstt = typing.List
        A generic version of list.
    
    MMAAPPPPIINNGG__FFIILLEE = PosixPath('/workspace/Fundalyze/config/term_mapping.jso...
    OOppttiioonnaall = typing.Optional
        Optional[X] is equivalent to Union[X, None].
    
    PPRROOJJEECCTT__RROOOOTT = PosixPath('/workspace/Fundalyze')

FFIILLEE
    /workspace/Fundalyze/modules/data/term_mapper.py


```

## modules.data.compare
```
Python Library Documentation: module modules.data.compare in modules.data

NNAAMMEE
    modules.data.compare - Utilities for comparing company profiles from OpenBB and yfinance.

FFUUNNCCTTIIOONNSS
    ddiiffff__ddiicctt(d1: Dict, d2: Dict) -> Dict[str, Tuple]
        Return dictionary of differing keys and their values.
    
    ffeettcchh__pprrooffiillee__ooppeennbbbb(symbol: str) -> pandas.core.frame.DataFrame
        Fetch company profile via OpenBB. Returns empty DataFrame on error.
    
    ffeettcchh__pprrooffiillee__yyff(symbol: str) -> pandas.core.frame.DataFrame
        Fetch company profile via yfinance. Returns empty DataFrame on error.
    
    iinntteerraaccttiivvee__pprrooffiillee(symbol: str) -> pandas.core.frame.DataFrame
        Fetch profile from OpenBB and yfinance, compare and prompt user to choose.
    
    iiss__ccoommpplleettee(df: pandas.core.frame.DataFrame) -> bool
        Return True if DataFrame has essential columns and is non-empty.

DDAATTAA
    DDiicctt = typing.Dict
        A generic version of dict.
    
    EESSSSEENNTTIIAALL__CCOOLLSS = ['longName', 'sector', 'industry', 'marketCap', 'webs...
    TTuuppllee = typing.Tuple
        Deprecated alias to builtins.tuple.
        
        Tuple[X, Y] is the cross-product type of X and Y.
        
        Example: Tuple[T1, T2] is a tuple of two elements corresponding
        to type variables T1 and T2.  Tuple[int, float, str] is a tuple
        of an int, a float and a string.
        
        To specify a variable-length tuple of homogeneous type, use Tuple[T, ...].
    
    llooggggeerr = <Logger modules.data.compare (WARNING)>

FFIILLEE
    /workspace/Fundalyze/modules/data/compare.py


```

## modules.utils.data_utils
```
Python Library Documentation: module modules.utils.data_utils in modules.utils

NNAAMMEE
    modules.utils.data_utils - Utility helpers for pandas data processing.

FFUUNNCCTTIIOONNSS
    eennssuurree__ppeerriioodd__ccoolluummnn(df: 'pd.DataFrame', column_name: 'str' = 'Period') -> 'pd.DataFrame'
        Ensure ``df`` has a period column by resetting index if needed.
    
    rreeaadd__ccssvv__iiff__eexxiissttss(path: 'Path', **kwargs) -> 'Optional[pd.DataFrame]'
        Return DataFrame from ``path`` if the file exists else ``None``.
    
    rreeaadd__jjssoonn__iiff__eexxiissttss(path: 'Path') -> 'Optional[Any]'
        Return deserialized JSON object from ``path`` if it exists.
    
    ssttrriipp__ttiimmeezzoonneess(df: 'pd.DataFrame') -> 'pd.DataFrame'
        Return copy of ``df`` with timezone information removed.
    
    wwrriittee__ddaattaaffrraammee(df: 'pd.DataFrame', csv_path: 'Path', *, write_csv: 'bool' = True, write_json: 'bool' = False) -> 'None'
        Save ``df`` to CSV and/or JSON using ``csv_path`` as base path.

DDAATTAA
    OOppttiioonnaall = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FFIILLEE
    /workspace/Fundalyze/modules/utils/data_utils.py


```

## modules.utils.excel_utils
```
Python Library Documentation: module modules.utils.excel_utils in modules.utils

NNAAMMEE
    modules.utils.excel_utils

FFUUNNCCTTIIOONNSS
    ccooll__ttoo__lleetttteerr(idx: 'int') -> 'str'
        Return Excel-style column letters (0-based).
    
    wwrriittee__ttaabbllee(writer: 'pd.ExcelWriter', df: 'pd.DataFrame', sheet_name: 'str', table_name: 'str', *, style: 'str' = 'Table Style Medium 2') -> 'None'
        Write ``df`` to ``sheet_name`` and convert it to a formatted table.

FFIILLEE
    /workspace/Fundalyze/modules/utils/excel_utils.py


```

## modules.utils.math_utils
```
Python Library Documentation: module modules.utils.math_utils in modules.utils

NNAAMMEE
    modules.utils.math_utils

FFUUNNCCTTIIOONNSS
    mmoovviinngg__aavveerraaggee(series: 'pd.Series', window: 'int') -> 'pd.Series'
        Return rolling mean over ``window`` periods.
    
    ppeerrcceennttaaggee__cchhaannggee(series: 'pd.Series', periods: 'int' = 1) -> 'pd.Series'
        Return percent change from ``periods`` prior values.

FFIILLEE
    /workspace/Fundalyze/modules/utils/math_utils.py


```

## modules.utils.progress_utils
```
Python Library Documentation: module modules.utils.progress_utils in modules.utils

NNAAMMEE
    modules.utils.progress_utils

FFUUNNCCTTIIOONNSS
    pprrooggrreessss__iitteerr(iterable: 'Iterable[T]', *, description: 'Optional[str]' = None) -> 'Iterator[T]'
        Yield items from ``iterable`` while displaying a progress bar if possible.
        
        Parameters
        ----------
        iterable:
            Any iterable sequence of values.
        description:
            Optional label shown alongside the progress bar.
        
        Returns
        -------
        Iterator[T]
            Iterator over the original values.

DDAATTAA
    IItteerraabbllee = typing.Iterable
        A generic version of collections.abc.Iterable.
    
    IItteerraattoorr = typing.Iterator
        A generic version of collections.abc.Iterator.
    
    OOppttiioonnaall = typing.Optional
        Optional[X] is equivalent to Union[X, None].
    
    TT = ~T

FFIILLEE
    /workspace/Fundalyze/modules/utils/progress_utils.py


```

## modules.logging_utils
```
Python Library Documentation: module modules.logging_utils in modules

NNAAMMEE
    modules.logging_utils - Logging configuration helpers.

FFUUNNCCTTIIOONNSS
    sseettuupp__llooggggiinngg(log_file: str = 'fundalyze.log', level: int = 10) -> None
        Configure root logger to log to console and ``log_file``.
        
        Parameters
        ----------
        log_file:
            File path where logs will be written. Directory will be created if
            needed.
        level:
            Logging level for the root logger.

FFIILLEE
    /workspace/Fundalyze/modules/logging_utils.py


```

## modules.interface
```
Python Library Documentation: module modules.interface in modules

NNAAMMEE
    modules.interface - Common CLI interface helpers used across modules.

FFUUNNCCTTIIOONNSS
    iinnppuutt__oorr__ccaanncceell(prompt: 'str') -> 'str'
        Return user input or an empty string if canceled.
    
    pprriinntt__hheeaaddeerr(title: 'str') -> 'None'
        Display a section heading consistently across menus.
    
    pprriinntt__iinnvvaalliidd__cchhooiiccee() -> 'None'
        Standard message for invalid menu selections.
    
    pprriinntt__mmeennuu(options: 'list[str]') -> 'None'
        Display a numbered menu list.
    
    pprriinntt__ttaabbllee(df: 'pd.DataFrame', *, showindex: 'bool' = False) -> 'None'
        Pretty-print a DataFrame using :mod:`tabulate`.

DDAATTAA
    IINNVVAALLIIDD__CCHHOOIICCEE__MMSSGG = "Invalid choice. Enter a number from the menu or ...

FFIILLEE
    /workspace/Fundalyze/modules/interface.py


```

