import json
import sys
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import yaml

from sklearn.preprocessing import StandardScaler
import joblib

from utils.seed import set_seed


def load_financial_csv(file_path: Path) -> pd.DataFrame:
    """Load and clean a financial CSV file."""
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]  # Clean headers

    # Clean dollar signs and convert to float
    for col in ["Close/Last", "Open", "High", "Low"]:
        df[col] = df[col].replace({r"\$": ""}, regex=True).astype(float)

    df["Volume"] = df["Volume"].astype(float)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=False)
    df.sort_values("Date", inplace=True)

    return df

def add_return_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add percentage variation (returns) based on Close/Last."""
    df = df.sort_values("Date").copy()
    df["Return"] = df["Close/Last"].pct_change() * 100
    df.dropna(inplace=True)
    return df

def add_features(df):
    df = df.sort_values("Date").copy()

    # Simple Moving Averages
    df["SMA_5"] = df["Close/Last"].rolling(5).mean()
    df["SMA_10"] = df["Close/Last"].rolling(10).mean()

    # Exponential Moving Average
    df["EMA_5"] = df["Close/Last"].ewm(span=5, adjust=False).mean()

    # Price Range / Volatility proxy
    df["High_Low_Spread"] = df["High"] - df["Low"]

    # Ratio-based features
    df["Open_Close_Ratio"] = df["Open"] / df["Close/Last"]

    # Volume-based returns
    df["Volume_Change"] = df["Volume"].pct_change()

    df.dropna(inplace=True)
    return df


def get_preview_plot(data_dict: dict[str, pd.DataFrame]) -> plt.Figure:
    """Plot preview of closing prices for a few companies."""
    fig = plt.figure(figsize=(10, 5), tight_layout=True)
    for i, (name, df) in enumerate(list(data_dict.items())[:2]):
        plt.plot(df["Date"], df["Return"], label=name)
    plt.plot(df["Date"], df["Return"], label=name)
    plt.ylabel("Daily Return (%)")
    plt.title("Stock Return Preview")
    plt.legend()
    return fig


def split_dataset(df: pd.DataFrame, split_ratio: float, seed: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split data into train/test based on date."""
    df = df.sort_values("Date")
    n = len(df)
    split_idx = int(n * (1 - split_ratio))
    df_train = df.iloc[:split_idx]
    df_test = df.iloc[split_idx:]
    return df_train, df_test


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 prepare_financial_data.py <raw-dataset-folder> <prepared-dataset-folder>\n")
        exit(1)

    # Load parameters
    prepare_params = yaml.safe_load(open("params.yaml"))["prepare"]

    raw_dataset_folder = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    seed = prepare_params["seed"]
    split = prepare_params["split"]

    # Optional test mode to create an artificial train/test time split
    # between the baseline dataset ("raw") and the newer candidate dataset
    # ("raw_candidate"). The cutoff date is defined by test_year/test_month.
    # - Baseline (non-candidate) data will use dates strictly BEFORE this cutoff.
    # - Candidate data will use dates FROM this cutoff onward.
    test_mode = prepare_params.get("test_mode", False)
    test_month = prepare_params.get("test_month")
    test_year = prepare_params.get("test_year")

    # Heuristic: only apply test mode on the newer dataset folder
    is_new_dataset = "candidate" in str(raw_dataset_folder)

    # Set seed for reproducibility
    set_seed(seed)

    # Load all company CSVs
    data_dict = {}
    for csv_file in raw_dataset_folder.glob("*.csv"):
        company_name = csv_file.stem
        df = load_financial_csv(csv_file)
        df = add_return_column(df)
        df = add_features(df)

        if test_mode and test_month is not None and test_year is not None:
            start_date = pd.Timestamp(year=int(test_year), month=int(test_month), day=1)

            if is_new_dataset:
                # Candidate dataset: keep data FROM the cutoff onward
                df = df[df["Date"] >= start_date].sort_values("Date")
                if df.empty:
                    print(
                        f"Warning: no data for {company_name} from {start_date.date()} onward. "
                        "Skipping this company in test mode."
                    )
                    continue
            else:
                # Baseline dataset: keep data strictly BEFORE the cutoff
                df = df[df["Date"] < start_date].sort_values("Date")
                if df.empty:
                    print(
                        f"Warning: no data for {company_name} before {start_date.date()} when "
                        "preparing baseline data in test mode. Skipping this company."
                    )
                    continue
        data_dict[company_name] = df

    if not prepared_dataset_folder.exists():
        prepared_dataset_folder.mkdir(parents=True)

    # Save preview plot
    preview_plot = get_preview_plot(data_dict)
    preview_plot.savefig(prepared_dataset_folder / "preview.png")

    # Normalize and split
    train_data, test_data = {}, {}
    for name, df in data_dict.items():
        df_train, df_test = split_dataset(df, split, seed)

        feature_cols = [
            "Return",
            "SMA_5",
            "SMA_10",
            "EMA_5",
            "High_Low_Spread",
            "Open_Close_Ratio",
            "Volume_Change",
        ]

        scaler = StandardScaler()
        df_train[feature_cols] = scaler.fit_transform(df_train[feature_cols])
        df_test[feature_cols] = scaler.transform(df_test[feature_cols])

        train_data[name] = df_train
        test_data[name] = df_test

        # Save per-company CSVs
        df_train.to_csv(prepared_dataset_folder / f"{name}_train.csv", index=False)
        df_test.to_csv(prepared_dataset_folder / f"{name}_test.csv", index=False)

        # Save scaler
        joblib.dump(scaler, prepared_dataset_folder / f"{name}_scaler.pkl")

    # Save metadata
    with open(prepared_dataset_folder / "companies.json", "w") as f:
        json.dump(list(data_dict.keys()), f)

    print(f"\nPrepared data saved at {prepared_dataset_folder.absolute()}")


if __name__ == "__main__":
    main()
