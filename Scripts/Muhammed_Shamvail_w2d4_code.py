import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("📊 SuperStore Dashboard")

uploaded_file = st.file_uploader(
    "Upload Superstore CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    @st.cache_data
    def load_data(file):
        return pd.read_csv(
            file,
            parse_dates=["order_date", "ship_date"]
        )

    df = load_data(uploaded_file)

    # Sidebar Filters
    with st.sidebar:
        st.header("Filters")

        regions = st.multiselect(
            "Region",
            options=df["Region"].unique(),
            default=df["Region"].unique()
        )

        years = st.multiselect(
            "Year",
            options=sorted(df["order_year"].unique()),
            default=sorted(df["order_year"].unique())
        )

        with st.form("date_filter"):

            start_date = st.date_input(
                "Start Date",
                df["order_date"].min().date()
            )

            end_date = st.date_input(
                "End Date",
                df["order_date"].max().date()
            )

            submitted = st.form_submit_button("Apply")

    # Filtering Data
    filtered_df = df[
        (df["Region"].isin(regions)) &
        (df["order_year"].isin(years))
    ]

    if submitted:
        filtered_df = filtered_df[
            filtered_df["order_date"]
            .dt.date.between(start_date, end_date)
        ]

    # =========================
    # Quality Alert Calculations
    # =========================

    disc_arr = filtered_df["discount"].to_numpy()
    sales_arr = filtered_df["sales"].to_numpy()

    high_disc_pct = np.percentile(disc_arr, 75)
    high_disc_n = (disc_arr > high_disc_pct).sum()

    mean_sales = sales_arr.mean()
    std_sales = sales_arr.std()

    if std_sales == 0:
        z_scores = np.zeros_like(sales_arr)
    else:
        z_scores = (sales_arr - mean_sales) / std_sales

    outlier_n = (np.abs(z_scores) > 2).sum()

    mean_margin = filtered_df["profit_margin_percent"].mean()

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sales",
        f"${filtered_df['sales'].sum():,.0f}"
    )

    col2.metric(
        "Total Profit",
        f"${filtered_df['profit'].sum():,.0f}"
    )

    col3.metric(
        "Average Discount",
        f"{filtered_df['discount'].mean() * 100:.1f}%"
    )

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Overview",
            "📦 By Category",
            "🌍 By Region",
            "🚨 Quality Alerts"
        ]
    )

    # ====================
    # Tab 1 - Overview
    # ====================

    with tab1:

        st.subheader("Data Preview")

        st.dataframe(
            filtered_df.head(20),
            use_container_width=True
        )

        monthly = (
            filtered_df
            .groupby(
                [
                    filtered_df["order_date"]
                    .dt.to_period("M")
                    .astype(str),
                    "order_year"
                ]
            )["sales"]
            .sum()
            .reset_index()
        )

        monthly.columns = [
            "Month",
            "order_year",
            "Sales"
        ]

        fig = px.line(
            monthly,
            x="Month",
            y="Sales",
            color="order_year",
            title="Year-over-Year Monthly Sales"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ====================
    # Tab 2 - Category
    # ====================

    with tab2:

        st.subheader(
            "Top 10 Sub-Categories by Sales"
        )

        top10 = (
            filtered_df
            .groupby("sub_category")["sales"]
            .sum()
            .nlargest(10)
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(7, 4)
        )

        bars = ax.barh(
            top10.index,
            top10.values
        )

        ax.bar_label(
            bars,
            fmt="$%.0f"
        )

        ax.set_xlabel("Sales")

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

        st.subheader(
            "Sales vs Profit"
        )

        fig = px.scatter(
            filtered_df,
            x="sales",
            y="profit",
            color="category",
            size="quantity",
            hover_data=["sub_category"],
            title="Sales vs Profit by Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ====================
    # Tab 3 - Region
    # ====================

    with tab3:

        st.subheader(
            "Profit Share by Region"
        )

        region_profit = (
            filtered_df
            .groupby("Region")["profit"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            region_profit,
            names="Region",
            values="profit",
            hole=0.4,
            title="Region-wise Profit Share"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ====================
    # Tab 4 - Quality Alerts
    # ====================

    with tab4:

        st.subheader("Quality Alerts")

        # Margin Health
        if mean_margin < 10:
            st.error(
                f"Low profit margin: {mean_margin:.1f}%"
            )

        elif mean_margin < 20:
            st.warning(
                f"Average profit margin: {mean_margin:.1f}%"
            )

        else:
            st.success(
                f"Healthy profit margin: {mean_margin:.1f}%"
            )

        # High Discount Alert
        st.info(
            f"{high_disc_n} orders have discount above "
            f"the 75th percentile "
            f"({high_disc_pct * 100:.1f}%)"
        )

        # Outlier Alert
        if outlier_n > 0:
            st.warning(
                f"{outlier_n} sales outliers detected."
            )

        else:
            st.success(
                "No sales outliers detected."
            )

        # Outlier Table
        with st.expander(
            "View outlier rows"
        ):

            outlier_mask = (
                np.abs(z_scores) > 2
            )

            outlier_rows = filtered_df[
                outlier_mask
            ][
                [
                    "order_id",
                    "order_date",
                    "sales",
                    "profit",
                    "Region"
                ]
            ]

            st.dataframe(
                outlier_rows,
                use_container_width=True
            )

    # Footer
    st.markdown("---")

    st.caption(
        f"Showing {len(filtered_df):,} rows • "
        f"{filtered_df['order_date'].min().year}-"
        f"{filtered_df['order_date'].max().year} • "
        f"Built by Muhammed Shamvail"
    )

else:

    st.info(
        "Please upload superstore_clean.csv to continue."
    )