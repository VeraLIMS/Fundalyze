# API Reference
Help on package modules.analytics in modules:

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


Help on module modules.generate_report.report_generator in modules.generate_report:

NAME
    modules.generate_report.report_generator - script: report_generator.py

DESCRIPTION
    Dependencies:
        pip install openbb[all] matplotlib pandas
    
    Usage:
        python src/report_generator.py AAPL MSFT GOOGL

FUNCTIONS
    fetch_and_compile(symbol: 'str', base_output: 'str | None' = None, *, price_period: 'str' = '1mo', statements: 'list[str] | None' = None, local_output: 'bool | None' = None) -> 'None'
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


Help on module modules.generate_report.excel_dashboard in modules.generate_report:

NAME
    modules.generate_report.excel_dashboard - # src/generate_report/excel_dashboard.py

FUNCTIONS
    create_and_open_dashboard(output_root: str | None = None, *, tickers: Optional[Iterable[str]] = None, progress: bool = False)
        Create an Excel dashboard (with named Tables) and open it automatically.
        
        Parameters
        ----------
        output_root:
            Base folder containing ticker subdirectories.
        tickers:
            Optional subset of tickers to include.
        progress:
            When ``True`` display a progress bar while loading CSV files.
    
    create_dashboard(output_root: str | None = None, *, tickers: Optional[Iterable[str]] = None, progress: bool = False) -> pathlib.Path
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
    
    show_dashboard_in_excel(dashboard_path: pathlib.Path)
        Open the newly created Excel file in the OS default application.

DATA
    Iterable = typing.Iterable
        A generic version of collections.abc.Iterable.
    
    Optional = typing.Optional
        Optional[X] is equivalent to Union[X, None].

FILE
    /workspace/Fundalyze/modules/generate_report/excel_dashboard.py


