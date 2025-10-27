import json
import sys
from pathlib import Path
from typing import Tuple, Dict

import numpy as np
import pandas as pd
import tensorflow as tf
import yaml
import bentoml

from utils.seed import set_seed


def load_financial_data(prepared_folder: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load and concatenate all company CSVs into train/test sets."""
    train_dfs, test_dfs = [], []

    for train_file in prepared_folder.glob("*_train.csv"):
        test_file = prepared_folder / train_file.name.replace("_train.csv", "_test.csv")

        df_train = pd.read_csv(train_file)
        df_test = pd.read_csv(test_file)

        # Ensure date is sorted (time order)
        df_train.sort_values("Date", inplace=True)
        df_test.sort_values("Date", inplace=True)

        # Features: Open, High, Low, Volume
        X_train = df_train[["Open", "High", "Low", "Volume"]].values
        X_test = df_test[["Open", "High", "Low", "Volume"]].values

        # Target: Close/Last
        y_train = df_train["Close/Last"].values
        y_test = df_test["Close/Last"].values

        train_dfs.append((X_train, y_train))
        test_dfs.append((X_test, y_test))

    # Concatenate all companies
    X_train = np.concatenate([x for x, _ in train_dfs])
    y_train = np.concatenate([y for _, y in train_dfs])
    X_test = np.concatenate([x for x, _ in test_dfs])
    y_test = np.concatenate([y for _, y in test_dfs])

    return X_train, y_train, X_test, y_test


def get_regression_model(input_dim: int, hidden_size: int) -> tf.keras.Model:
    """Simple dense regression model for stock price prediction."""
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_dim,)),
        tf.keras.layers.Dense(hidden_size, activation="relu"),
        tf.keras.layers.Dense(hidden_size // 2, activation="relu"),
        tf.keras.layers.Dense(1)  # predict close price
    ])
    return model


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 train_financial_model.py <prepared-dataset-folder> <model-folder>\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))
    prepare_params = params["prepare"]
    train_params = params["train"]

    prepared_dataset_folder = Path(sys.argv[1])
    model_folder = Path(sys.argv[2])

    seed = train_params["seed"]
    lr = train_params["lr"]
    epochs = train_params["epochs"]
    hidden_size = train_params["hidden_size"]

    # Set seed for reproducibility
    set_seed(seed)

    # Load data
    X_train, y_train, X_test, y_test = load_financial_data(prepared_dataset_folder)
    print(f"Loaded {len(X_train)} training samples, {len(X_test)} test samples")

    # Define model
    model = get_regression_model(input_dim=X_train.shape[1], hidden_size=hidden_size)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss="mse",
        metrics=["mae"]
    )
    model.summary()

    # Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=32,
        verbose=1
    )

    # Save model folder
    model_folder.mkdir(parents=True, exist_ok=True)

    # Define BentoML preprocess/postprocess
    def preprocess(x: Dict[str, float]):
        """Convert JSON input (Open, High, Low, Volume) to model input array."""
        return np.array([[x["Open"], x["High"], x["Low"], x["Volume"]]], dtype=np.float32)

    def postprocess(pred):
        """Convert model prediction to JSON."""
        return {"predicted_close": float(pred[0][0])}

    # Save the model with BentoML
    bentoml.keras.save_model(
        "financial_forecast_model",
        model,
        include_optimizer=True,
        custom_objects={
            "preprocess": preprocess,
            "postprocess": postprocess,
        }
    )

    bentoml.models.export_model(
        "financial_forecast_model:latest",
        f"{model_folder}/financial_forecast_model.bentomodel",
    )

    # Save training history
    np.save(model_folder / "history.npy", history.history)
    print(f"\nModel saved at {model_folder.absolute()}")


if __name__ == "__main__":
    main()
