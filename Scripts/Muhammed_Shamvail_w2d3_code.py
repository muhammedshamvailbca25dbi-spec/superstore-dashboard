import streamlit as st
import pandas as pd
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


    filtered_df = df[
        (df["Region"].isin(regions)) &
        (df["order_year"].isin(years))
    ]

    if submitted:
        filtered_df = filtered_df[
            filtered_df["order_date"]
            .dt.date.between(start_date, end_date)
        ]


    # KPI Row
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
        f"{filtered_df['discount'].mean()*100:.1f}%"
    )


    # Tabs
    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Overview",
            "📦 By Category",
            "🌍 By Region"
        ]
    )



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