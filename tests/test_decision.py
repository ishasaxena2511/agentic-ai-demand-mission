import pandas as pd
from agents.schema_agent import SchemaIntelligenceAgent
from agents.forecasting_agent import ForecastingAgent
from agents.decision_agent import DecisionAgent

# Load data
df = pd.read_csv("data/electronics_data.csv")

# Step A: Schema
schema = SchemaIntelligenceAgent(df).analyze()

# Step B: Forecast
forecast_agent = ForecastingAgent(
    df=df,
    date_col=schema["date_columns"][0],
    target_col=schema["demand_target"],
    product_col=schema["product_columns"][0],
    region_col=schema["region_columns"][0]
)

forecast_result = forecast_agent.forecast(
    horizon=30,
    product="Laptop",
    region="Maharashtra"
)

# Step C: Decision
decision_agent = DecisionAgent(
    forecast_values=forecast_result["forecast"].values,
    confidence=forecast_result["confidence"],
    horizon=30
)

decision = decision_agent.decide()
print(decision)
