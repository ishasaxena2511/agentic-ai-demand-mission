import pandas as pd
import numpy as np

class SchemaIntelligenceAgent:
    """
    Agent responsible for understanding unknown / messy CSV files.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.schema = {}

    # -----------------------------
    # Public entry
    # -----------------------------
    def analyze(self):
        self._detect_columns()
        self._detect_target()
        self._basic_health_check()
        return self.schema

    # -----------------------------
    # Column detection (ROBUST)
    # -----------------------------
    def _detect_columns(self):
        date_cols = []
        numeric_cols = []
        categorical_cols = []

        for col in self.df.columns:

            # Step 1: numeric check FIRST
            if pd.api.types.is_numeric_dtype(self.df[col]):
                numeric_cols.append(col)
                continue

            # Step 2: datetime check ONLY for non-numeric
            if self._is_datetime(col):
                date_cols.append(col)
            else:
                categorical_cols.append(col)

        self.schema["date_columns"] = date_cols
        self.schema["numeric_columns"] = numeric_cols
        self.schema["categorical_columns"] = categorical_cols

        # Semantic inference
        self.schema["region_columns"] = [
            c for c in categorical_cols
            if any(k in c.lower() for k in ["state", "city", "region", "location"])
        ]

        self.schema["product_columns"] = [
            c for c in categorical_cols
            if any(k in c.lower() for k in ["product", "item", "category", "type"])
        ]

    # -----------------------------
    # Demand target inference
    # -----------------------------
    def _detect_target(self):
        numeric_cols = self.schema.get("numeric_columns", [])

        if not numeric_cols:
            self.schema["demand_target"] = None
            return

        variances = {}
        for col in numeric_cols:
            series = self.df[col].dropna()
            if len(series) > 1:
                variances[col] = series.var()

        if not variances:
            self.schema["demand_target"] = None
            return

        demand_target = max(variances, key=variances.get)
        self.schema["demand_target"] = demand_target
        self.schema["target_variance"] = round(variances[demand_target], 2)

    # -----------------------------
    # Data health checks
    # -----------------------------
    def _basic_health_check(self):
        self.schema["row_count"] = len(self.df)
        self.schema["column_count"] = len(self.df.columns)

        self.schema["missing_values"] = {
            col: int(self.df[col].isna().sum())
            for col in self.df.columns
            if self.df[col].isna().sum() > 0
        }

        self.schema["duplicate_rows"] = int(self.df.duplicated().sum())

    # -----------------------------
    # Safe datetime detection
    # -----------------------------
    def _is_datetime(self, col):
        try:
            parsed = pd.to_datetime(self.df[col], errors="coerce")
            success_ratio = parsed.notna().mean()

            # At least 80% valid datetime values
            return success_ratio > 0.8
        except Exception:
            return False
