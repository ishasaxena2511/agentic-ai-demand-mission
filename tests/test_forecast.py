import pandas as pd
from agents.schema_agent import SchemaIntelligenceAgent
from agents.forecasting_agent import ForecastingAgent

df = pd.read_csv("data/electronics_data.csv")

# Step A: schema detection
schema = SchemaIntelligenceAgent(df).analyze()

# Step B: forecasting
agent = ForecastingAgent(
    df=df,
    date_col=schema["date_columns"][0],
    target_col=schema["demand_target"],
    product_col=schema["product_columns"][0],
    region_col=schema["region_columns"][0]
)

result = agent.forecast(
    horizon=30,
    product="Laptop",
    region="Maharashtra"
)

print(result["forecast"].head())
