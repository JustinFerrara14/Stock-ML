import json
import pandas as pd
from pathlib import Path

# Paths
folder_path = Path("./doc/samplePrediction")
csv_path = folder_path / "stock_data.csv"
output_json = folder_path / "stock_data_input.json"

# Load CSV
df = pd.read_csv(csv_path)
df.columns = [c.strip() for c in df.columns]

# Clean numeric columns
for col in ["Close/Last", "Open", "High", "Low"]:
    df[col] = df[col].replace({'\$': ''}, regex=True).astype(float)

df["Volume"] = df["Volume"].astype(float)
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values("Date", inplace=True)

# --- Feature engineering (same as prepare.py) ---

# Returns
df["Return"] = df["Close/Last"].pct_change() * 100

# Moving averages
df["SMA_5"] = df["Close/Last"].rolling(5).mean()
df["SMA_10"] = df["Close/Last"].rolling(10).mean()
df["EMA_5"] = df["Close/Last"].ewm(span=5, adjust=False).mean()

# Volatility proxy
df["High_Low_Spread"] = df["High"] - df["Low"]

# Ratios
df["Open_Close_Ratio"] = df["Open"] / df["Close/Last"]

# Volume change
df["Volume_Change"] = df["Volume"].pct_change()

# Drop NaNs created by rolling/pct_change
df.dropna(inplace=True)

FEATURE_COLS = [
    "Return",
    "SMA_5",
    "SMA_10",
    "EMA_5",
    "High_Low_Spread",
    "Open_Close_Ratio",
    "Volume_Change",
]

# Take last 60 rows
df_last_60 = df.tail(60)[FEATURE_COLS]

# Convert to JSON format
result = {
    "stock_data": df_last_60.to_dict(orient="records")
}

# Save JSON
with open(output_json, "w") as f:
    json.dump(result, f, indent=2)

print("JSON generated from last 60 values")
