import json
import sys
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
import yaml

from utils.seed import set_seed


def load_financial_csv(file_path: Path) -> pd.DataFrame:
    """Load and clean a financial CSV file."""
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]  # Clean headers

    # Clean dollar signs and convert to float
    for col in ["Close/Last", "Open", "High", "Low"]:
        df[col] = df[col].replace({'\$': ''}, regex=True).astype(float)

    df["Volume"] = df["Volume"].astype(float)
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)

    return df


def get_preview_plot(data_dict: dict[str, pd.DataFrame]) -> plt.Figure:
    """Plot preview of closing prices for a few companies."""
    fig = plt.figure(figsize=(10, 5), tight_layout=True)
    for i, (name, df) in enumerate(list(data_dict.items())[:5]):
        plt.plot(df["Date"], df["Close/Last"], label=name)
    plt.xlabel("Date")
    plt.ylabel("Close Price ($)")
    plt.title("Stock Price Preview")
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

    # Set seed for reproducibility
    set_seed(seed)

    # Load all company CSVs
    data_dict = {}
    for csv_file in raw_dataset_folder.glob("*.csv"):
        company_name = csv_file.stem
        df = load_financial_csv(csv_file)
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

        # Normalize numeric columns (except Date)
        numeric_cols = ["Close/Last", "Open", "High", "Low", "Volume"]
        df_train[numeric_cols] = (df_train[numeric_cols] - df_train[numeric_cols].mean()) / df_train[numeric_cols].std()
        df_test[numeric_cols] = (df_test[numeric_cols] - df_train[numeric_cols].mean()) / df_train[numeric_cols].std()

        train_data[name] = df_train
        test_data[name] = df_test

        # Save per-company CSVs
        df_train.to_csv(prepared_dataset_folder / f"{name}_train.csv", index=False)
        df_test.to_csv(prepared_dataset_folder / f"{name}_test.csv", index=False)

    # Save metadata
    with open(prepared_dataset_folder / "companies.json", "w") as f:
        json.dump(list(data_dict.keys()), f)

    print(f"\nPrepared data saved at {prepared_dataset_folder.absolute()}")


if __name__ == "__main__":
    main()
