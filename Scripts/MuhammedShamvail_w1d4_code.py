import streamlit as st
import pandas as pd
import datetime

st.title("💳 Personal Expense Tracker")
st.write("Upload and analyze your personal expenses.")

file = st.file_uploader("Upload expenses.csv", type="csv")

if file is None:
    st.info("Upload expenses.csv to get started.")

else:
    df = pd.read_csv(file)

    df["Date"] = pd.to_datetime(df["Date"])

    st.sidebar.header("Filters")

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(
            datetime.date(2024, 1, 1),
            datetime.date(2024, 5, 31)
        )
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    categories = [
        "Food & Dining",
        "Transport",
        "Utilities",
        "Entertainment",
        "Healthcare",
        "Shopping"
    ]

    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        categories,
        default=categories
    )

    if len(selected_categories) == 0:
        selected_categories = categories

    filtered_df = df[
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ]

    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

    total_spend = filtered_df["Amount"].sum()
    transactions = len(filtered_df)
    average = filtered_df["Amount"].mean()
    largest = filtered_df["Amount"].max()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Spend", f"₹{total_spend:.2f}")
    col2.metric("Transactions", transactions)
    col3.metric("Average", f"₹{average:.2f}")
    col4.metric("Largest", f"₹{largest:.2f}")

    st.subheader("Filtered Transactions")

    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "Download Filtered CSV",
        filtered_df.to_csv(index=False),
        file_name=f"expenses_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

    st.subheader("Spend by Category")

    color = st.color_picker(
        "Pick a Bar Colour",
        "#3B82F6"
    )

    st.write("Selected Colour:", color)

    category_spend = (
        filtered_df.groupby("Category")["Amount"]
        .sum()
    )

    st.bar_chart(category_spend)

    st.subheader("Monthly Summary")

    monthly_summary = (
        filtered_df.groupby(
            filtered_df["Date"].dt.month_name()
        )
        .agg(
            Total_Spend=("Amount", "sum"),
            Transactions=("Amount", "count")
        )
    )

    st.table(monthly_summary)

    st.markdown("---")

    st.caption(
        f"Muhammed Shamvail | Personal Expense Tracker | {datetime.date.today()}"
    )