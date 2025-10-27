import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import bentoml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def get_training_plot(model_history: dict) -> plt.Figure:
    """Plot training and validation loss"""
    epochs = range(1, len(model_history["loss"]) + 1)
    fig = plt.figure(figsize=(10, 4))
    plt.plot(epochs, model_history["loss"], label="Training loss")
    plt.plot(epochs, model_history["val_loss"], label="Validation loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss (MSE)")
    plt.title("Training and Validation Loss")
    plt.legend()
    plt.grid(True)
    return fig


def get_prediction_plot(y_true, y_pred) -> plt.Figure:
    """Scatter plot: True vs Predicted closing prices"""
    fig = plt.figure(figsize=(6, 6))
    plt.scatter(y_true, y_pred, alpha=0.6)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "r--", lw=2)
    plt.xlabel("True Close Price")
    plt.ylabel("Predicted Close Price")
    plt.title("True vs Predicted Close Prices")
    plt.grid(True)
    return fig


def get_residuals_plot(y_true, y_pred) -> plt.Figure:
    """Histogram of residuals"""
    residuals = y_true - y_pred
    fig = plt.figure(figsize=(8, 4))
    plt.hist(residuals, bins=40, edgecolor="black", alpha=0.7)
    plt.title("Residuals Distribution")
    plt.xlabel("Prediction Error")
    plt.ylabel("Frequency")
    plt.grid(True)
    return fig


def load_test_data(prepared_folder: Path):
    """Load all *_test.csv files into one combined DataFrame"""
    dfs = []
    for test_file in prepared_folder.glob("*_test.csv"):
        df = pd.read_csv(test_file)
        df.sort_values("Date", inplace=True)
        dfs.append(df)
    df_all = pd.concat(dfs, ignore_index=True)
    X = df_all[["Open", "High", "Low", "Volume"]].values
    y = df_all["Close/Last"].values
    return X, y


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

    # Load test data
    X_test, y_test = load_test_data(prepared_dataset_folder)
    print(f"Loaded {len(X_test)} test samples")

    # Import and load model from BentoML
    model_name = "financial_forecast_model"
    try:
        bentoml.models.import_model(f"{model_folder}/{model_name}.bentomodel")
    except bentoml.exceptions.BentoMLException:
        print("Model already exists in the BentoML store, skipping import.")

    model = bentoml.keras.load_model(model_name)
    model_history = np.load(model_folder / "history.npy", allow_pickle=True).item()

    # Predict
    y_pred = model.predict(X_test).flatten()

    # Compute metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"Validation MAE:  {mae:.4f}")
    print(f"Validation RMSE: {rmse:.4f}")
    print(f"R² Score:        {r2:.4f}")

    # Save metrics
    with open(evaluation_folder / "metrics.json", "w") as f:
        json.dump({"mae": mae, "rmse": rmse, "r2": r2}, f, indent=4)

    # Save plots
    get_training_plot(model_history).savefig(plots_folder / "training_history.png")
    get_prediction_plot(y_test, y_pred).savefig(plots_folder / "pred_vs_true.png")
    get_residuals_plot(y_test, y_pred).savefig(plots_folder / "residuals.png")

    print(f"\nEvaluation results saved in {evaluation_folder.absolute()}")


if __name__ == "__main__":
    main()
