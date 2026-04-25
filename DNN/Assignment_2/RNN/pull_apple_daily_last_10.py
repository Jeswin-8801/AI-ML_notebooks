import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def get_clean_stock_data(ticker="AAPL", years=10):
    print(f"--- Step 1: Downloading {ticker} Data ---")

    # Calculate dates
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=years * 365)).strftime("%Y-%m-%d")

    # Download data
    # We use auto_adjust=True to get 'Close' as the split-adjusted price automatically
    raw_data = yf.download(
        ticker, start=start_date, end=end_date, interval="1d", auto_adjust=True
    )

    print(f"--- Step 2: Cleaning Headers ---")

    # Many versions of yfinance return a multi-index header (Price, Ticker)
    # We flatten it so it's just 'Close', 'Open', etc.
    if isinstance(raw_data.columns, pd.MultiIndex):
        raw_data.columns = raw_data.columns.get_level_values(0)

    # Reset index to turn 'Date' from an index into a regular column
    clean_df = raw_data.reset_index()

    # Rename 'Close' to 'Adj Close' for clarity (since it is adjusted)
    clean_df = clean_df.rename(columns={"Close": "Adj_Close"})

    # Ensure columns are in a standard order
    columns_order = ["Date", "Adj_Close", "Open", "High", "Low", "Volume"]
    clean_df = clean_df[columns_order]

    print(f"--- Step 3: Saving to CSV ---")
    filename = f"{ticker}_cleaned_data.csv"
    clean_df.to_csv(filename, index=False)

    print(f"Success! Saved {len(clean_df)} rows to {filename}")
    return clean_df


# --- EXECUTION ---
# 1. Download and Clean
df = get_clean_stock_data("AAPL", 10)

# 2. Verify the result
print("\nFinal Cleaned Data Structure:")
print(df.head())
print("\nColumn Names Check:", df.columns.tolist())
