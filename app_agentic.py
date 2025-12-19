import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

from agents.schema_agent import SchemaIntelligenceAgent
from agents.forecasting_agent import ForecastingAgent
from agents.decision_agent import DecisionAgent
from agents.geo_navigation_agent import GeoNavigationAgent, CITY_COORDS


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Agentic AI Demand & Mission Planner",
    layout="wide"
)
st.title("🤖 Agentic AI: Demand Intelligence & Mission Planning")

NAV_CITIES = sorted(CITY_COORDS.keys())


# ==================================================
# FILE UPLOAD
# ==================================================
uploaded_file = st.sidebar.file_uploader("📂 Upload Sales CSV", type=["csv"])
if uploaded_file is None:
    st.info("Upload a CSV file to begin analysis.")
    st.stop()

df = pd.read_csv(uploaded_file)


# ==================================================
# SCHEMA INTELLIGENCE
# ==================================================
schema = SchemaIntelligenceAgent(df).analyze()

date_col = schema["date_columns"][0]
target_col = schema["demand_target"]
product_col = schema["product_columns"][0]
region_col = schema["region_columns"][0]


# ==================================================
# DEMAND AGGREGATION
# ==================================================
product_demand = (
    df.groupby(product_col)[target_col]
    .sum()
    .reset_index()
    .sort_values(by=target_col, ascending=False)
)
product_demand["Rank"] = range(1, len(product_demand) + 1)
product_demand["Rank"] = product_demand["Rank"].astype(int)

region_demand = (
    df.groupby(region_col)[target_col]
    .sum()
    .reset_index()
    .sort_values(by=target_col, ascending=False)
)


# ==================================================
# 📈 KEY BUSINESS METRICS
# ==================================================
best_product = product_demand.iloc[0][product_col]
best_region = region_demand.iloc[0][region_col]

filtered_df = df[
    (df[product_col] == best_product) &
    (df[region_col] == best_region)
]

total_demand = int(filtered_df[target_col].sum())

half = len(filtered_df) // 2
growth = (
    (filtered_df[target_col].iloc[half:].sum()
     - filtered_df[target_col].iloc[:half].sum())
    / max(filtered_df[target_col].sum(), 1)
) * 100

risk = (
    "High"
    if filtered_df[target_col].std() > filtered_df[target_col].mean()
    else "Medium"
)

forecast_agent = ForecastingAgent(
    df, date_col, target_col, product_col, region_col
)

forecast_30 = forecast_agent.forecast(30, best_product, best_region)
confidence = forecast_30["confidence"]

st.subheader("📈 Key Business Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Demand", f"{total_demand} units")
c2.metric("Demand Growth", f"{growth:.1f}%")
c3.metric("Risk Level", risk)
c4.metric("AI Confidence", confidence)


# ==================================================
# 📊 DEMAND INTELLIGENCE DASHBOARD
# ==================================================
st.subheader("📊 Demand Intelligence Dashboard")

st.dataframe(
    product_demand[["Rank", product_col, target_col]]
    .rename(columns={product_col: "Product", target_col: "Total Demand"}),
    use_container_width=True
)

st.plotly_chart(
    px.bar(
        product_demand.head(5),
        x=product_col,
        y=target_col,
        title="Top Products by Total Demand"
    ),
    use_container_width=True
)

st.plotly_chart(
    px.bar(
        region_demand.head(5),
        x=region_col,
        y=target_col,
        title="Top Regions by Total Demand"
    ),
    use_container_width=True
)

heatmap_df = (
    df.groupby([product_col, region_col])[target_col]
    .sum()
    .reset_index()
)

st.plotly_chart(
    px.density_heatmap(
        heatmap_df,
        x=region_col,
        y=product_col,
        z=target_col,
        title="Product × Region Demand Heatmap",
        color_continuous_scale="Viridis"
    ),
    use_container_width=True
)


# ==================================================
# 🔮 FUTURE DEMAND FORECAST
# ==================================================
st.subheader("🔮 Future Demand Forecast")

forecast_days = st.selectbox(
    "📆 Select Forecast Horizon (days)",
    [3, 7, 15, 30, 60, 90],
    index=3
)

forecast_result = forecast_agent.forecast(
    forecast_days, best_product, best_region
)

history_df = forecast_result["history"].reset_index()
history_df.columns = ["Date", "Demand"]
history_df["Type"] = "Historical"

future_df = forecast_result["forecast"].reset_index()
future_df.columns = ["Date", "Demand"]
future_df["Type"] = "Forecast"

plot_df = pd.concat([history_df, future_df], ignore_index=True)

fig = px.line(
    plot_df,
    x="Date",
    y="Demand",
    color="Type",
    markers=True,
    title=f"Demand Forecast — {best_product} in {best_region}"
)

st.plotly_chart(fig, use_container_width=True)

# ---- SINGLE SOURCE OF TRUTH ----
forecast_series = future_df["Demand"].astype(float)
avg_future_demand = round(float(forecast_series.mean()), 2)
peak_future_demand = round(float(forecast_series.max()), 2)

st.success(
    f"""
📌 **How to read this forecast**

• Average demand over next **{forecast_days} days**: **{avg_future_demand} units/day**  
• Peak expected demand: **{peak_future_demand} units/day**
"""
)


# ==================================================
# 🧠 AI ACTION PLAN — GROUPED (NO PRODUCT REPETITION)
# ==================================================
st.subheader("🧠 AI Action Plan — What to Sell, Where & How Much")

rows = []
rank = 1

for _, p_row in product_demand.iterrows():
    product = p_row[product_col]

    city_df = (
        df[df[product_col] == product]
        .groupby(region_col)[target_col]
        .sum()
        .reset_index()
        .sort_values(by=target_col, ascending=False)
    )

    first_row = True

    for _, c_row in city_df.iterrows():
        demand = int(c_row[target_col])
        if demand <= 0:
            continue

        if demand > 200:
            conf = "High"
            action = "Stock aggressively"
        elif demand > 120:
            conf = "Medium"
            action = "Ensure availability"
        elif demand > 60:
            conf = "Medium"
            action = "Targeted supply"
        else:
            conf = "Low"
            action = "Limited stock"

        rows.append({
            "Rank": rank if first_row else "",
            "Product": product if first_row else "",
            "City / Region": c_row[region_col],
            "Est. Demand (units)": demand,
            "Confidence": conf,
            "Recommended Action": action
        })

        first_row = False

    rank += 1

action_plan_df = pd.DataFrame(rows)

st.dataframe(
    action_plan_df,
    use_container_width=True,
    height=500,
    hide_index=True
)


# ==================================================
# 🧠 AI DECISION ENGINE (BACKEND)
# ==================================================
decision = DecisionAgent(
    forecast_series.values,
    confidence,
    forecast_days
).decide()


# ==================================================
# 🧠 AI DECISION SUMMARY (HUMAN-CENTRIC)
# ==================================================
st.subheader("🧠 AI Decision Summary (Business Insight)")

if decision["decision"] == "NO_MISSION":
    st.info(
        f"""
**What the data suggests**

Demand exists but is **not yet strong or stable**.

• Avg forecasted demand: **{avg_future_demand} units/day**
• Confidence: **{confidence}**
• Risk level: **{risk}**

This looks like a **monitoring or pilot phase**, not a failure.
"""
    )
else:
    st.success(
        f"""
**What the data suggests**

Demand patterns are **strong and repeatable**.

• Avg forecasted demand: **{avg_future_demand} units/day**
• Peak demand: **{peak_future_demand} units/day**
• Confidence: **{confidence}**

This supports planning — not mandatory action.
"""
    )


# ==================================================
# 🗺️ HUB-BASED ROUTE OPTIMIZATION
# ==================================================
if decision["decision"] != "NO_MISSION":

    st.subheader("🗺️ Hub-Based Mission Route Optimization")

    warehouse = st.selectbox("📦 Select Warehouse Location", NAV_CITIES)

    service_hubs = []
    for r in region_demand[region_col]:
        if r in NAV_CITIES and r != warehouse:
            service_hubs.append(r)
        if len(service_hubs) == 3:
            break

    if service_hubs:
        fuel_price = st.slider("Fuel Price (₹ / litre)", 80, 120, 100)

        route = GeoNavigationAgent().plan_multi_stop_route(
            [warehouse] + service_hubs,
            fuel_price
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Distance (km)", route["distance_km"])
        c2.metric("ETA (hours)", route["eta_hours"])
        c3.metric("Fuel Cost (₹)", route["fuel_cost"])

        st.write("**Optimized Route:**")
        st.write(" → ".join(route["path"]))

        components.html(route["map"]._repr_html_(), height=500)

    else:
        st.warning("No serviceable hubs found for routing.")

