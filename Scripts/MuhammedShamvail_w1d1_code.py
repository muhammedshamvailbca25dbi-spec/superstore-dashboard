import streamlit as st
st.title("Muhammed Shamvail ")

st.header('About Me', divider='blue')
st.markdown("My name is Muhammed Shamvail. I am currently pursuing a Bachelor of Computer Applications (BCA) in Artificial Intelligence and Machine Learning with Data Science. I am passionate about technology, AI, programming, and learning new skills. I enjoy exploring innovative ideas, working on projects, and improving my knowledge in software development and data science. My goal is to build a successful career in the technology field and continuously grow as a professional.")

st.header('Skills', divider='green')
st.markdown("- **Time Management**\n - **Python Programming**\n- **Data Analysis**\n **Quick Learning Ability** ")


st.header('Contact', divider='orange')

st.write("📧 Email: muhammedshamvail@gmail.com ")
st.subheader('Code ', help='A pattern I use often')
st.code("""
import pandas as pd
df = pd.read_csv("data.csv")
print(df.describe())
""", language="python")
st.subheader('Formula')
st.latex(r'\text{Profit Margin} = \frac{\text{Profit}}{\text(Sales)}')

st.markdown('---')
st.caption('Built with Streamlit · Day 1 Project · 2026')

