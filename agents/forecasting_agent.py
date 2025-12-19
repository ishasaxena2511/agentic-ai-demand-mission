import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class ForecastingAgent:
    """
    Agent responsible for forecasting future demand
    with intelligent fallbacks for sparse data.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        date_col: str,
        target_col: str,
        product_col: str = None,
        region_col: str = None
    ):
        self.df = df.copy()
        self.date_col = date_col
        self.target_col = target_col
        self.product_col = product_col
        self.region_col = region_col

        self.df[self.date_col] = pd.to_datetime(self.df[self.date_col])
        self.df = self.df.sort_values(self.date_col)

    # -----------------------------
    # Main forecasting entry
    # -----------------------------
    def forecast(
        self,
        horizon: int = 30,
        product: str = None,
        region: str = None
    ):
        data = self.df.copy()

        # Apply filters
        if self.product_col and product:
            data = data[data[self.product_col] == product]

        if self.region_col and region:
            data = data[data[self.region_col] == region]

        # Try multiple aggregation levels
        for freq in ["D", "W", "ME"]:
            ts = self._aggregate(data, freq)

            if len(ts) >= 8:
                forecast = self._ets_forecast(ts, horizon, freq)
                return {
                    "history": ts,
                    "forecast": forecast,
                    "frequency": freq,
                    "confidence": self._confidence_label(freq)
                }

        # Final fallback: naive forecast
        ts = self._aggregate(data, "D")
        forecast = self._naive_forecast(ts, horizon)

        return {
            "history": ts,
            "forecast": forecast,
            "frequency": "naive",
            "confidence": "Low"
        }

    # -----------------------------
    # Aggregation helper
    # -----------------------------
    def _aggregate(self, data, freq):
        ts = (
            data
            .groupby(pd.Grouper(key=self.date_col, freq=freq))[self.target_col]
            .sum()
            .fillna(0)
        )
        return ts

    # -----------------------------
    # ETS forecasting
    # -----------------------------
    def _ets_forecast(self, ts, horizon, freq):
        model = ExponentialSmoothing(
            ts,
            trend="add",
            seasonal=None
        )
        fitted = model.fit()
        forecast = fitted.forecast(horizon)

        return forecast

    # -----------------------------
    # Naive fallback
    # -----------------------------
    def _naive_forecast(self, ts, horizon):
        if len(ts) == 0:
            return pd.Series([0] * horizon)

        mean_value = ts.mean()
        index = pd.date_range(
            start=ts.index.max(),
            periods=horizon + 1,
            freq="D"
        )[1:]

        return pd.Series([mean_value] * horizon, index=index)

    # -----------------------------
    # Confidence heuristic
    # -----------------------------
    def _confidence_label(self, freq):
        if freq == "D":
            return "High"
        if freq == "W":
            return "Medium"
        if freq == "M":
            return "Low"
        return "Low"
