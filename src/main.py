import yfinance as yf
import pandas as pd
import os

def fetch_and_display(symbol: str):
    """
    1) Fetch basic company info and print selected fields.
    2) Download and print 1 month of price history.
    3) Fetch annual and quarterly financial statements and print/save them.
    """
    print(f"\n=== Processing {symbol} ===")
    ticker = yf.Ticker(symbol)

    # 1) Company Info
    try:
        info = ticker.info
    except Exception as e:
        print(f"  Error fetching info: {e}")
        return

    if not info or info.get("longName") is None:
        print(f"  No company info available for {symbol}.")
    else:
        print(f"  Long Name : {info.get('longName')}")
        print(f"  Sector    : {info.get('sector')}")
        print(f"  Industry  : {info.get('industry')}")
        print(f"  Market Cap: {info.get('marketCap'):,}")
        print(f"  Website   : {info.get('website')}")

    # 2) Recent Price History (last 1 month)
    try:
        hist = ticker.history(period="1mo")
    except Exception as e:
        print(f"  Error fetching price history: {e}")
        hist = pd.DataFrame()

    if hist.empty:
        print(f"  No price history available for the past month.")
    else:
        hist_df = hist.drop(columns=[col for col in ["Dividends", "Stock Splits"] if col in hist.columns])
        print("\n  Last 5 rows of price history (1 month):")
        print(hist_df.tail(5).to_string())

        # Save to CSV
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, f"{symbol}_1mo_prices.csv")
        hist_df.to_csv(csv_path)
        print(f"  → Saved 1-month price history to: {csv_path}")

    # 3) Annual & Quarterly Financial Statements
    fetch_and_save_financial_statement(ticker, symbol, statement="financials", label="Annual Income Statement")
    fetch_and_save_financial_statement(ticker, symbol, statement="quarterly_financials", label="Quarterly Income Statement")
    fetch_and_save_financial_statement(ticker, symbol, statement="balance_sheet", label="Annual Balance Sheet")
    fetch_and_save_financial_statement(ticker, symbol, statement="quarterly_balance_sheet", label="Quarterly Balance Sheet")
    fetch_and_save_financial_statement(ticker, symbol, statement="cashflow", label="Annual Cash Flow")
    fetch_and_save_financial_statement(ticker, symbol, statement="quarterly_cashflow", label="Quarterly Cash Flow")


def fetch_and_save_financial_statement(ticker_obj, symbol: str, statement: str, label: str):
    """
    Attempts to fetch the DataFrame for `statement` (e.g. 'financials', 'balance_sheet', etc.).
    If data is present, prints the top 3 rows and saves to CSV under /src/output/<symbol>_<statement>.csv.
    If empty or error, prints a message.
    """
    try:
        df = getattr(ticker_obj, statement)
    except Exception as e:
        print(f"\n  Error fetching {label}: {e}")
        return

    if isinstance(df, pd.DataFrame) and not df.empty:
        print(f"\n  {label} (first 3 rows):")
        print(df.head(3).to_string())

        # Save to CSV
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{symbol}_{statement}.csv"
        filepath = os.path.join(output_dir, filename)

        # If columns are dates (years/periods), transpose so rows are dates before saving
        try:
            if any(isinstance(col, pd.Timestamp) for col in df.columns):
                df_to_save = df.T
            else:
                df_to_save = df
        except Exception:
            df_to_save = df

        df_to_save.to_csv(filepath)
        print(f"  → Saved {label} to: {filepath}")
    else:
        print(f"\n  {label} not available or empty for {symbol}.")


if __name__ == "__main__":
    """
    Instead of a hard-coded list, ask the user which ticker(s) to fetch.
    Example input:  PARTN.SW, MSFT, GOOGL
    """
    raw_input = input("Enter ticker symbol(s), separated by commas (e.g. PARTN.SW, MSFT): ").strip()
    # Split on commas and strip whitespace, ignoring empty entries
    symbols_to_fetch = [s.strip() for s in raw_input.split(",") if s.strip()]

    if not symbols_to_fetch:
        print("No valid ticker symbols entered. Exiting.")
    else:
        for sym in symbols_to_fetch:
            fetch_and_display(sym)
