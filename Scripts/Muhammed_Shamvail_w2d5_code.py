import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="📊",
    layout="wide"
)


@st.cache_data(ttl=600)
def load_data():
    return pd.read_csv(
        r"Data/superstore_clean.csv",
        parse_dates=["order_date", "ship_date"]
    )

try:
    df = load_data()
    if st.sidebar.button("🔄️ Refresh data"):
        st.cache_data.clear()
        st.rerun()
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()


st.title("📊 Superstore Dashboard")
st.markdown("Interactive dashboard for Superstore sales analysis")

df["order_year"] = df["order_date"].dt.year

df["month_period"] = df["order_date"].dt.strftime("%b")


with st.sidebar:

    st.header("Filters")

    selected_regions = st.multiselect(
        "Region",
        options=sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

    selected_years = st.multiselect(
        "Year",
        options=sorted(df["order_year"].unique()),
        default=sorted(df["order_year"].unique())
    )

    start_date = st.date_input(
        "Start Date",
        value=df["order_date"].min().date()
    )

    end_date = st.date_input(
        "End Date",
        value=df["order_date"].max().date()
    )

filtered = df[
    (df["Region"].isin(selected_regions)) &
    (df["order_year"].isin(selected_years))
]

filtered = filtered[
    filtered["order_date"].dt.date.between(
        start_date,
        end_date
    )
]

filtered["month_period"] = filtered["order_date"].dt.strftime("%b")


st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        f"${filtered['sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${filtered['profit'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Average Discount",
        f"{filtered['discount'].mean():.1%}"
    )


col1, col2 = st.columns(2)

with col1:

    st.subheader("Sales by Category")

    category_sales = (
        filtered.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

with col2:

    st.subheader("Profit by Category")

    category_profit = (
        filtered.groupby("category")["profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_profit)



st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered.groupby(
        filtered["order_date"].dt.to_period("M")
    )["sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)



st.subheader("Filtered Data")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)



csv_bytes = filtered.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    "📥 Download Filtered Data",
    data=csv_bytes,
    file_name="superstore_filtered.csv",
    mime="text/csv"
)
st.subheader("Custom Chart Generator")

with st.form("chart_form"):

    chart_type = st.selectbox(
        "Choose Chart Type",
        ["Bar", "Line", "Pie"]
    )

    submitted = st.form_submit_button(
        "Generate Chart"
    )


if submitted:

    chart_data = (
        filtered.groupby("category")["sales"]
        .sum()
        .reset_index()
    )

    if chart_type == "Bar":

        fig = px.bar(
            chart_data,
            x="category",
            y="sales",
            title="Sales by Category - Bar Chart"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    elif chart_type == "Line":

        fig = px.line(
            chart_data,
            x="category",
            y="sales",
            markers=True,
            title="Sales by Category - Line Chart"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    elif chart_type == "Pie":

        fig = px.pie(
            chart_data,
            names="category",
            values="sales",
            title="Sales Distribution by Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


tab1, tab2, tab3,tab4 = st.tabs(
    [
        "📋 Overview",
        "📦 By Category",
        "🗺️ By Region",
        "🚨Quality Alerts"
    ]
)


with tab1:
    st.subheader("Filtered Data Preview")

    monthly_sales = (
    filtered.groupby(["order_year", "month_period"], as_index=False)["sales"]
      .sum()
    )

    fig = px.line(
    monthly_sales,
    x="month_period",
    y="sales",
    color="order_year",
    title="Monthly Sales Trend by Category"
    )
    st.plotly_chart(fig, use_container_width=True)


with tab2:
    st.subheader("Sales by Category")

    top10_subcat = (
    filtered.groupby("sub_category")["sales"]
      .sum()
      .nlargest(10)          
      .sort_values()         
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.barh(
    top10_subcat.index,
    top10_subcat.values, 
    color="#3B82F6"

    )

    ax.bar_label(
    bars,
    fmt="${:,.0f}",
    padding=4,
    fontsize=8
    )

    ax.set_title("Top 10 Sub-Categories by Sales")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Sub-Category")

    st.pyplot(fig)
    plt.close(fig)

    fig = px.scatter(
    filtered,
    x="sales",
    y="profit",
    color="category",          
    size="quantity",          
    hover_data=["sub_category"],
    title="Sales vs Profit by Category"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sub-Category Breakdown")

    subcategory_summary = (
        filtered.groupby("sub_category")
        .agg(
            Total_Sales=("sales", "sum"),
            Total_Profit=("profit", "sum")
        )
        .sort_values(
            by="Total_Sales",
            ascending=False
        )
    )

    st.dataframe(
        subcategory_summary.style.format("${:,.0f}"),
        use_container_width=True
    )


with tab3:

    st.subheader("Sales by Region")

    region_profit = (
        filtered.groupby("Region")["profit"]
          .sum()
          .reset_index()
    )

    fig = px.pie(
        region_profit,
        names="Region",
        values="profit",
        hole=0.4,
        title="Region Share of Total Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Quality Alert")

    disc_arr = filtered["discount"].values
    p75 = np.percentile(disc_arr, 75)
    high_disc = filtered[disc_arr > p75]
    high_disc_n = len(high_disc)

    st.info(
        f"{high_disc_n} orders have discount above the 75th percentile "
        f"({p75:.0%})."
    )

    st.subheader("Profit Margin Alert")
    total_sales = filtered["sales"].sum()
    total_profit = filtered["profit"].sum()

    if total_sales > 0:
        profit_margin = (total_profit / total_sales) * 100
    else:
        profit_margin = 0.0

    margin_formatted = f"{profit_margin:.1f}%"

    if profit_margin < 10:
        st.error(f"Low Profit Margin! Current margin is {margin_formatted}.")
    elif profit_margin < 20:
        st.warning(f"Moderate Profit Margin. Current margin is {margin_formatted}.")
    else:
        st.success(f"Healthy Profit Margin! Current margin is {margin_formatted}.")

    
    sales_arr = filtered["sales"].values
    z_scores = (sales_arr - sales_arr.mean()) / sales_arr.std()
    outlier_mask = np.abs(z_scores) > 3
    outlier_rows = filtered[outlier_mask][["order_id", "order_date", "sales", "profit", "Region"]]
    outlier_n = len(outlier_rows)

    if outlier_n > 0:
        st.warning(f"{outlier_n} outlier order(s) detected with unusually high or low sales (|z-score| > 3).")
    else:
        st.success("No sales outliers detected.")

    with st.expander("View Outlier Rows"):
        st.dataframe(outlier_rows, use_container_width=True, hide_index=True)

    with st.expander("Show Raw Data (First 50 Rows):"):
        st.dataframe(filtered.head(50), use_container_width=True)




st.markdown("---")

row_count = len(filtered)

min_year = filtered["order_year"].min()
max_year = filtered["order_year"].max()

st.caption(
    f"Showing {row_count:,} rows • "
    f"{min_year}–{max_year} • "
    f"Built by Muhammed Shamvail"
)