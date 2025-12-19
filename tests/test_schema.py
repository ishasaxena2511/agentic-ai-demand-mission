# test_schema.py
import pandas as pd
from agents.schema_agent import SchemaIntelligenceAgent

df = pd.read_csv("data/electronics_data.csv")
agent = SchemaIntelligenceAgent(df)
schema = agent.analyze()
print(schema)
