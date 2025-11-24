from __future__ import annotations
from bentoml.validators import ContentType
from typing import Annotated, List, Dict
from pydantic import Field
import bentoml
import json
import numpy as np

@bentoml.service(name="stock-ml")
class FinancialForecastService:
    # Load the trained BentoML model
    bento_model = bentoml.models.get("stock-ml")

    def __init__(self) -> None:
        # Custom preprocess/postprocess functions from the saved model
        self.preprocess = self.bento_model.custom_objects["preprocess"]
        self.postprocess = self.bento_model.custom_objects["postprocess"]
        self.model = self.bento_model.load_model()

    @bentoml.api()
    def predict(
            self,
            stock_data: Annotated[
                List[Dict[str, float]],
                ContentType("application/json")
            ] = Field(
                description=(
                    "Last 60 days of stock data. Each dict must contain "
                    "'Return', 'SMA_5', 'SMA_10', 'EMA_5', 'High_Low_Spread', 'Open_Close_Ratio', 'Volume_Change'."
                )
            ),
    ) -> Annotated[Dict[str, list], ContentType("application/json")]:
        """
        Example input:
        {
            "stock_data": [
                {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
                ...
            ]
        }
        """

        try:
            input_len = 60  # must match training input length
            if len(stock_data) != input_len:
                raise ValueError(f"Input data must contain exactly {input_len} days of stock data, actually got {len(stock_data)} days.")

            # Preprocess input to model-ready shape
            X = self.preprocess(stock_data)  # shape: (1, input_len, 4)

            # Make prediction
            y_pred = self.model.predict(X)

            # Postprocess to JSON-friendly dict
            return self.postprocess(y_pred)
        except Exception as e:
            return {"error": str(e)}
