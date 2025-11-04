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
        features = df[["Return"]].values
        target = df["Return"].values
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

def plot_forecast_example(y_true, y_pred, X_test, sample_idx=0):
    """
    Show previous 30 days (input) + next 5 days (true vs predicted).
    X_test: input sequences (30-day returns)
    y_true: true next 5-day returns
    y_pred: predicted next 5-day returns
    """
    past_returns = X_test[sample_idx].flatten()
    true_future = y_true[sample_idx]
    pred_future = y_pred[sample_idx]

    # Combine for full timeline
    days = np.arange(len(past_returns) + len(true_future))
    fig = plt.figure(figsize=(10, 5))
    plt.plot(days[:len(past_returns)], past_returns, label="Past 30d Returns", color="gray", linestyle="--")
    plt.plot([len(past_returns)-1, len(past_returns)], [past_returns[-1], true_future[0]], color="gray", linestyle="--") # transition line
    plt.plot(days[len(past_returns):], true_future, marker="o", label="True Next 5d", color="green")
    plt.plot(days[len(past_returns):], pred_future, marker="x", label="Predicted Next 5d", color="orange")

    plt.title(f"Stock Return Forecast Example (Sample {sample_idx})")
    plt.xlabel("Days (Past 30 + Next 5)")
    plt.ylabel("Return (%)")
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

    # Compute metrics with price scale
    mae = mean_absolute_error(y_test.flatten(), y_pred.flatten())
    mse = mean_squared_error(y_test.flatten(), y_pred.flatten())
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test.flatten(), y_pred.flatten())

    print(f"Validation MAE:  {mae:.4f}")
    print(f"Validation RMSE: {rmse:.4f}")
    print(f"R² Score:        {r2:.4f}")

    # Compute per-sample RMSE
    sample_errors = np.sqrt(np.mean((y_pred - y_test) ** 2, axis=1))

    # Get indices of 2 best and 2 worst predictions
    best_indices = np.argsort(sample_errors)[:2]
    worst_indices = np.argsort(sample_errors)[-2:]

    # Create plots
    for idx in best_indices:
        fig = plot_forecast_example(y_test, y_pred, X_test, sample_idx=idx)
        fig.suptitle(f"Best Prediction Example (idx={idx}, RMSE={sample_errors[idx]:.2f})")
        fig.savefig(plots_folder / f"best_prediction_{idx}.png")
        plt.close(fig)

    for idx in worst_indices:
        fig = plot_forecast_example(y_test, y_pred, X_test, sample_idx=idx)
        fig.suptitle(f"Worst Prediction Example (idx={idx}, RMSE={sample_errors[idx]:.2f})")
        fig.savefig(plots_folder / f"worst_prediction_{idx}.png")
        plt.close(fig)

    with open(evaluation_folder / "metrics.json", "w") as f:
        json.dump({"mae": mae, "rmse": rmse, "r2": r2}, f, indent=4)

    plot_forecast_example(y_test, y_pred, X_test, sample_idx=idx).savefig(plots_folder / "forecast_example.png")

    print(f"\nEvaluation results saved in {evaluation_folder.absolute()}")


if __name__ == "__main__":
    main()
