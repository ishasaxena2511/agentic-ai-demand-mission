# 🤖 Agentic AI Demand Intelligence & Mission Planning System

An **Agentic AI-powered decision support system** that automatically analyzes messy sales data, forecasts future demand, and assists businesses in planning **what to sell, where to sell, and how much to distribute**, with optional inventory awareness and logistics routing.

This project is designed to simulate **real-world retail & supply chain intelligence**, not just theoretical predictions.

---

## 🚀 Key Highlights

- 📂 Works with **any CSV format** (no fixed schema required)
- 🧠 Automatically understands data structure (dates, products, regions, demand)
- 🔮 Forecasts demand for **3–90 day horizons**
- 📊 Transparent visual dashboards (bars, heatmaps, trends)
- 📦 Inventory-aware recommendations (manual input or inventory file upload)
- 🗺️ Hub-based mission route planning (no paid APIs)
- 👤 Human-centric AI insights (decision support, not commands)

---

## 🧩 Problem Statement

Businesses often struggle to:
- Understand **which products are in demand**
- Identify **where demand is emerging**
- Predict **future demand accurately**
- Allocate inventory efficiently under stock constraints
- Plan logistics without expensive APIs

This system addresses all of the above using **local, open-source AI models** and **agent-based intelligence**.

---

## 🧠 System Architecture (Agentic Design)

The system is built using multiple cooperating AI agents:

1. **Schema Intelligence Agent**
   - Detects date, product, region, and demand columns from any CSV
   - Handles messy, real-world datasets

2. **Forecasting Agent**
   - Performs time-series forecasting (Holt-Winters)
   - Supports flexible horizons: 3, 7, 15, 30, 60, 90 days

3. **Demand Intelligence Engine**
   - Aggregates product & region demand
   - Builds ranked insights and heatmaps

4. **Inventory Awareness Layer**
   - Accepts manual stock input OR inventory CSV
   - Adjusts recommendations based on available stock

5. **Decision Insight Agent**
   - Converts forecasts into **human-readable business insights**
   - Avoids commanding language (decision support only)

6. **Geo Navigation Agent**
   - Performs hub-based route optimization
   - Estimates distance, ETA, and fuel cost (offline)

---

## 📊 Features Overview

### 📈 Demand Intelligence Dashboard
- Top products by demand
- Top regions by demand
- Product × Region heatmap
- Key business metrics (growth, risk, confidence)

### 🔮 Future Demand Forecast
- Interactive forecast horizon selection
- Clear distinction between historical & predicted demand
- Average and peak demand interpretation

### 🧠 AI Action Plan (Core Feature)
- Ranked, non-repetitive product table
- City-wise breakdown per product
- Forecast-aware demand estimation
- Inventory-adjusted supply suggestions

### 📦 Inventory Integration (Optional)
- Manual stock input per product
- OR upload inventory CSV
- AI adapts recommendations automatically

### 🗺️ Mission Route Planning
- Warehouse selection
- AI-selected service hubs
- Distance, ETA, and fuel cost estimation
- Visual route map (offline)

---

🖥️ Tech Stack

Python
Streamlit – UI & dashboard
Pandas / NumPy – data processing
Statsmodels – demand forecasting
Plotly – interactive visualizations
NetworkX + Folium – routing & maps

No paid APIs used.

---

▶️ How to Run Locally (Windows)

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app_agentic.py

---

