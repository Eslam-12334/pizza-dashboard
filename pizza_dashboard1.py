import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- تحميل البيانات ----------------
merged = pd.read_csv(r"C:\Users\p&p\Desktop\merged_data3.csv")

# ---------------- تجهيز البيانات ----------------
merged["sales"] = merged["price"] * merged["quantity"]
merged["date"] = pd.to_datetime(merged["date"], errors="coerce")
merged["month"] = merged["date"].dt.to_period("M").astype(str)
merged["hour"] = merged["date"].dt.hour

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Pizza Sales Dashboard", layout="wide")
st.title("🍕 Pizza Store Sales Dashboard")

# ----------- الكروت الأساسية ----------- #
col1, col2, col3 = st.columns(3)
total_sales = merged["sales"].sum()
total_orders = merged["order_id"].nunique()
total_pizzas = merged["pizza_id"].nunique()

with col1:
    st.metric("💰 Total Sales", f"${total_sales:,.2f}")
with col2:
    st.metric("🛍️ Total Orders", total_orders)
with col3:
    st.metric("🍕 Pizza Types", total_pizzas)

st.divider()

# ----------- اختيار تحليل الوقت ----------- #
st.subheader("📊 Sales Trend")

option = st.radio(
    "Select Time Granularity:",
    ("Daily", "Monthly", "Hourly"),
    horizontal=True
)

if option == "Daily":
    data_to_plot = merged.groupby("date", as_index=False)["sales"].sum()
    fig = px.line(
        data_to_plot,
        x="date",
        y="sales",
        title="📅 Daily Sales Trend",
        markers=True
    )
elif option == "Monthly":
    data_to_plot = merged.groupby("month", as_index=False)["sales"].sum()
    fig = px.bar(
        data_to_plot,
        x="month",
        y="sales",
        title="📆 Monthly Sales Overview",
        text_auto=True,
        color="sales",
        color_continuous_scale="Blues"
    )
else:
    data_to_plot = merged.groupby("hour", as_index=False)["sales"].sum()
    fig = px.line(
        data_to_plot,
        x="hour",
        y="sales",
        title="⏰ Hourly Sales Trend",
        markers=True
    )

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------- أفضل 5 بيتزات مبيعًا ----------- #
st.subheader("🏆 Top 5 Best-Selling Pizzas")

if "name" in merged.columns:
    top_pizzas = merged.groupby("name", as_index=False)["sales"].sum()
else:
    top_pizzas = merged.groupby("pizza_id", as_index=False)["sales"].sum()

top_pizzas = top_pizzas.sort_values(by="sales", ascending=False).head(5)

fig_top = px.bar(
    top_pizzas,
    x="sales",
    y=top_pizzas.columns[0],
    orientation="h",
    text_auto=True,
    title="🔥 Top 5 Selling Pizzas",
    color="sales",
    color_continuous_scale="Oranges"
)

st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# ----------- المبيعات حسب الفئة ----------- #
st.subheader("🍴 Sales by Pizza Category")

if "category" in merged.columns:
    category_sales = merged.groupby("category", as_index=False)["sales"].sum()
    fig3 = px.pie(
        category_sales,
        names="category",
        values="sales",
        title="🍕 Sales by Category",
        hole=0.4
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("⚠️ No 'category' column found in the data.")


