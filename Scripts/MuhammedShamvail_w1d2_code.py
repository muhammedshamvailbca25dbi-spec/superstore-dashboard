import streamlit as st
import pandas as pd 


data = {
    'Name':
['Aisha','Bob','Clara','Dev','Eva','Finn','Grace','Hiro','Ines','Jay'],
    'Math':  [88, 52, 76, 91 , 43, 67, 85, 59, 78, 95],
    'Science': [72, 45, 88, 83, 38, 71, 90, 62, 55, 80],
    'English': [65, 70, 82, 77, 60, 58, 74, 88, 91, 73],
    'Art': [90, 85, 60, 55, 78, 92, 68, 75, 83, 61],
}
df = pd.DataFrame(data)
df['Average'] = df[['Math', 'Science', 'English', 'Art']].mean(axis=1).round(1)


st.title("📚 Student Performance Dashboard")

st.write(f"There are **{len(df)} students** in the class.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Class Average", f"{df['Average'].mean():.1f}")

with col2:
    st.metric("Highest Average", f"{df['Average'].max():.1f}")

with col3:
    st.metric("Lowest Average", f"{df['Average'].min():.1f}")

with col4:
    st.metric(
        "Average ≥ 70",
        len(df[df["Average"] >= 70])
    )


st.subheader("All Students")

def color_avg(val):
    if val >= 70:
        return "color: green"
    return "color: red"

styled_df = df.style.map(color_avg, subset=["Average"])

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)



st.subheader("🏆 Top 3 Students")

top3 = (
    df.sort_values("Average", ascending=False)
      .head(3)
      .reset_index(drop=True)
)

top3.index = top3.index + 1

st.table(top3)



st.subheader("📊 Subject Summary")

subjects = ["Math", "Science", "English", "Art"]

summary = {}

for subject in subjects:
    summary[subject] = {
        "Minimum Score": int(df[subject].min()),
        "Maximum Score": int(df[subject].max()),
        "Class Mean": round(df[subject].mean(), 1)
    }

st.json(summary)


st.divider()

import datetime

st.caption(
    f"Muhammed Shamvail | Student Dashboard Project | {datetime.date.today()}"
)