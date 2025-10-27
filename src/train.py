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


def create_sequences(df: pd.DataFrame, input_len, output_len):
    """Create sliding windows of input_len days to predict next output_len days."""
    features = df[["Open", "High", "Low", "Volume"]].values
    target = df["Close/Last"].values
    X, y = [], []

    for i in range(len(df) - input_len - output_len):
        X.append(features[i:i+input_len])
        y.append(target[i+input_len:i+input_len+output_len])
    return np.array(X), np.array(y)


def load_sequence_data(prepared_folder: Path, input_len, output_len) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load all companies' CSVs and create sequence-based train/test datasets."""
    X_train_list, y_train_list, X_test_list, y_test_list = [], [], [], []

    for train_file in prepared_folder.glob("*_train.csv"):
        test_file = prepared_folder / train_file.name.replace("_train.csv", "_test.csv")

        df_train = pd.read_csv(train_file)
        df_test = pd.read_csv(test_file)

        # Sort by date
        df_train.sort_values("Date", inplace=True)
        df_test.sort_values("Date", inplace=True)

        # Create input sequences (X) and targets (y)
        X_train, y_train = create_sequences(df_train, input_len, output_len)
        X_test, y_test = create_sequences(df_test, input_len, output_len)

        if len(X_train) > 0:
            X_train_list.append(X_train)
            y_train_list.append(y_train)
        if len(X_test) > 0:
            X_test_list.append(X_test)
            y_test_list.append(y_test)

    # Combine across companies
    X_train = np.concatenate(X_train_list)
    y_train = np.concatenate(y_train_list)
    X_test = np.concatenate(X_test_list)
    y_test = np.concatenate(y_test_list)

    return X_train, y_train, X_test, y_test


def get_sequence_model(input_len: int, input_dim: int, output_len: int, hidden_num_layers: int, hidden_size: int, dropout: float) -> tf.keras.Model:
    """LSTM model for next-5-day price prediction."""
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(input_len, input_dim)))
    for _ in range(hidden_num_layers):
        model.add(tf.keras.layers.LSTM(hidden_size, return_sequences=True, dropout=dropout))
    model.add(tf.keras.layers.LSTM(hidden_size, return_sequences=False, dropout=dropout))
    model.add(tf.keras.layers.Dense(output_len))  # predict next x days

    return model


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 train_financial_model.py <prepared-dataset-folder> <model-folder>\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))
    train_params = params["train"]

    prepared_dataset_folder = Path(sys.argv[1])
    model_folder = Path(sys.argv[2])

    seed = train_params["seed"]
    lr = train_params["lr"]
    epochs = train_params["epochs"]
    hidden_num_layers = train_params.get("hidden_num_layers", 2)
    hidden_size = train_params["hidden_size"]
    dropout = train_params.get("dropout")
    input_len = train_params["input_length"]
    output_len = train_params["output_length"]

    # Set reproducibility
    set_seed(seed)

    # Load data
    X_train, y_train, X_test, y_test = load_sequence_data(prepared_dataset_folder, input_len, output_len)
    print(f"Loaded {len(X_train)} train sequences, {len(X_test)} test sequences")

    # Build model
    model = get_sequence_model(
        input_len=X_train.shape[1],
        input_dim=X_train.shape[2],
        output_len=y_train.shape[1],
        hidden_num_layers=hidden_num_layers,
        hidden_size=hidden_size,
        dropout=dropout,
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss="mse",
        metrics=["mae"]
    )

    model.summary()

    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=32,
        verbose=1
    )

    # Save model
    model_folder.mkdir(parents=True, exist_ok=True)

    def preprocess(x: Dict[str, list]):
        """Preprocess last 30 days of input (dict with lists) for prediction."""
        arr = np.array([[v["Open"], v["High"], v["Low"], v["Volume"]] for v in x[-30:]])
        return np.expand_dims(arr, axis=0).astype(np.float32)

    def postprocess(pred):
        """Convert model output (5-day forecast) to JSON."""
        return {"predicted_close_next5": pred[0].tolist()}

    bentoml.keras.save_model(
        "financial_forecast_model_seq",
        model,
        include_optimizer=True,
        custom_objects={
            "preprocess": preprocess,
            "postprocess": postprocess,
        }
    )

    bentoml.models.export_model(
        "financial_forecast_model_seq:latest",
        f"{model_folder}/financial_forecast_model_seq.bentomodel",
    )

    np.save(model_folder / "history.npy", history.history)
    print(f"\nModel saved at {model_folder.absolute()}")


if __name__ == "__main__":
    main()
