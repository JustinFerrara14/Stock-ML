import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import bentoml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_test_sequences(prepared_folder: Path, input_len=30, output_len=5):
    """Load and build sequence-based test data."""
    def create_sequences(df):
        features = df[["Open", "High", "Low", "Volume"]].values
        target = df["Close/Last"].values
        X, y = [], []
        for i in range(len(df) - input_len - output_len):
            X.append(features[i:i+input_len])
            y.append(target[i+input_len:i+input_len+output_len])
        return np.array(X), np.array(y)

    Xs, ys = [], []
    for test_file in prepared_folder.glob("*_test.csv"):
        df = pd.read_csv(test_file)
        df.sort_values("Date", inplace=True)
        X, y = create_sequences(df)
        if len(X) > 0:
            Xs.append(X)
            ys.append(y)

    return np.concatenate(Xs), np.concatenate(ys)


def plot_forecast_example(y_true, y_pred, sample_idx=0):
    """Show true vs predicted 5-day forecast for one sample."""
    fig = plt.figure(figsize=(8, 4))
    plt.plot(range(5), y_true[sample_idx], marker="o", label="True")
    plt.plot(range(5), y_pred[sample_idx], marker="x", label="Predicted")
    plt.title("Next 5-Day Forecast (Example)")
    plt.xlabel("Day Ahead")
    plt.ylabel("Close Price (normalized)")
    plt.legend()
    plt.grid(True)
    return fig


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 evaluate_financial_model.py <model-folder> <prepared-dataset-folder>\n")
        exit(1)

    model_folder = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    evaluation_folder = Path("evaluation")
    plots_folder = evaluation_folder / "plots"

    plots_folder.mkdir(parents=True, exist_ok=True)

    X_test, y_test = load_test_sequences(prepared_dataset_folder)
    print(f"Loaded {len(X_test)} test sequences")

    model_name = "financial_forecast_model_seq"
    try:
        bentoml.models.import_model(f"{model_folder}/{model_name}.bentomodel")
    except bentoml.exceptions.BentoMLException:
        print("Model already exists in the BentoML store, skipping import.")

    model = bentoml.keras.load_model(model_name)
    model_history = np.load(model_folder / "history.npy", allow_pickle=True).item()

    # Predict on test set
    y_pred = model.predict(X_test)

    # Get normalized values
    norm_file = next(prepared_dataset_folder.glob("*_norm.json"))
    with open(norm_file, "r") as f:
        norm = json.load(f)

    mean = norm["mean"]["Close/Last"]
    std = norm["std"]["Close/Last"]

    # Denormalize
    y_test_real = y_test * std + mean
    y_pred_real = y_pred * std + mean

    # Compute metrics in real price scale
    mae = mean_absolute_error(y_test_real.flatten(), y_pred_real.flatten())
    mse = mean_squared_error(y_test_real.flatten(), y_pred_real.flatten())
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_real.flatten(), y_pred_real.flatten())

    print(f"Validation MAE:  {mae:.4f}")
    print(f"Validation RMSE: {rmse:.4f}")
    print(f"R² Score:        {r2:.4f}")

    with open(evaluation_folder / "metrics.json", "w") as f:
        json.dump({"mae": mae, "rmse": rmse, "r2": r2}, f, indent=4)

    plot_forecast_example(y_test, y_pred).savefig(plots_folder / "forecast_example.png")

    print(f"\nEvaluation results saved in {evaluation_folder.absolute()}")


if __name__ == "__main__":
    main()
