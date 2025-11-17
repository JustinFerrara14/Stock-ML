from __future__ import annotations
from bentoml.validators import ContentType
from typing import Annotated, List, Dict
from pydantic import Field
import bentoml
import json
import numpy as np

@bentoml.service(name="financial_forecast_service")
class FinancialForecastService:
    # Load the trained BentoML model
    bento_model = bentoml.keras.get("financial_forecast_model_seq")

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
                    "Last 30 days of stock data. Each dict must contain "
                    "'Open', 'High', 'Low', 'Volume'."
                )
            ),
    ) -> Annotated[Dict[str, list], ContentType("application/json")]:
        """
        Example input:
        [
            {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
            ...
            # 30 days
        ]
        """

        try:
            if len(stock_data) != 30:
                raise ValueError("Input data must contain exactly 30 days of stock data, actually got "
                                 f"{len(stock_data)} days.")

            # Preprocess input to model-ready shape
            X = self.preprocess(stock_data)  # shape: (1, 30, 4)

            # Make prediction
            y_pred = self.model.predict(X)

            # Postprocess to JSON-friendly dict
            return self.postprocess(y_pred)
        except Exception as e:
            return {"error": str(e)}
