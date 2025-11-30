import json
from pathlib import Path
from typing import List

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


FEATURE_COLUMNS: List[str] = [
    "Return",
    "SMA_5",
    "SMA_10",
    "EMA_5",
    "High_Low_Spread",
    "Open_Close_Ratio",
    "Volume_Change",
]


def load_prepared_folder(folder: Path) -> pd.DataFrame:

    dfs = []
    for csv_file in sorted(folder.glob("*_train.csv")):
        df = pd.read_csv(csv_file)
        # Keep only shared feature columns if present
        available_cols = [c for c in FEATURE_COLUMNS if c in df.columns]
        if not available_cols:
            continue
        dfs.append(df[available_cols])

    if not dfs:
        raise ValueError(f"No train CSV files with expected feature columns found in {folder}")

    return pd.concat(dfs, ignore_index=True)


def compute_drift_report(
    reference_folder: Path,
    current_folder: Path,
    output_html: Path,
    output_json: Path,
) -> None:

    reference_df = load_prepared_folder(reference_folder)
    current_df = load_prepared_folder(current_folder)

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)

    output_html.parent.mkdir(parents=True, exist_ok=True)
    report.save_html(str(output_html))

    result = report.as_dict()
    summary = {}

    try:
        data_drift = result["metrics"][0]["result"]["dataset_drift"]
        drift_share = result["metrics"][0]["result"].get("share_of_drifted_columns")
        n_features = result["metrics"][0]["result"].get("number_of_columns")
        summary = {
            "dataset_drift": bool(data_drift),
            "share_of_drifted_columns": drift_share,
            "number_of_columns": n_features,
        }
    except Exception:
        summary = {"raw": result}

    with output_json.open("w") as f:
        json.dump(summary, f, indent=4)


def main() -> None:
    """CLI entry point.

    Usage:
        python -m src.drift_analysis <reference_folder> <current_folder> <output_html> <output_json>
    """

    import sys

    if len(sys.argv) != 5:
        print("Arguments error. Usage:\n")
        print("\tpython3 drift_analysis.py <reference-folder> <current-folder> <output-html> <output-json>\n")
        sys.exit(1)

    reference_folder = Path(sys.argv[1])
    current_folder = Path(sys.argv[2])
    output_html = Path(sys.argv[3])
    output_json = Path(sys.argv[4])

    compute_drift_report(reference_folder, current_folder, output_html, output_json)


if __name__ == "__main__":
    main()
