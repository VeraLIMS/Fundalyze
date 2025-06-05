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


