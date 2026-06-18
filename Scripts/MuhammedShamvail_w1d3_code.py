import streamlit as st
import pandas as pd

st.title("⚖️ BMI & Health Calculator")
st.write(
    "Calculate your BMI, daily calorie needs, and ideal weight range."
)

st.markdown("---")

st.header("👤 Personal Details")

name = st.text_input("Enter your Name")

age = st.number_input(
    "Enter your Age",
    min_value=10,
    max_value=100,
    step=1
)

sex = st.radio(
    "Select Gender",
    ["Male", "Female"],
    horizontal=True
)

weight = st.slider(
    "Weight (kg)",
    min_value=30,
    max_value=150,
    step=1
)

height = st.slider(
    "Height (cm)",
    min_value=100,
    max_value=220,
    step=1
)

st.write(
    f"""
    **Name:** {name}

    **Age:** {age}

    **Gender:** {sex}

    **Weight:** {weight} kg

    **Height:** {height} cm
    """
)

st.markdown("---")

st.header("📊 BMI Calculator")

height_m = height / 100
bmi = weight / (height_m ** 2)

st.metric(
    "BMI",
    round(bmi, 1)
)

if bmi < 18.5:
    bmi_category = "Underweight"
    risk = "Moderate"
    st.warning(f"{bmi_category} | Health Risk: {risk}")

elif bmi < 25:
    bmi_category = "Normal Weight"
    risk = "Low"
    st.success(f"{bmi_category} | Health Risk: {risk}")

elif bmi < 30:
    bmi_category = "Overweight"
    risk = "Elevated"
    st.warning(f"{bmi_category} | Health Risk: {risk}")

else:
    bmi_category = "Obese"
    risk = "High"
    st.error(f"{bmi_category} | Health Risk: {risk}")

st.markdown("---")

st.header("🔥 Daily Calorie Need")

activity_options = {
    "Sedentary (desk job)": 1.2,
    "Lightly active (1-3 days/wk)": 1.375,
    "Moderately active (3-5 days)": 1.55,
    "Very active (6-7 days)": 1.725
}

activity = st.selectbox(
    "Select Activity Level",
    list(activity_options.keys())
)


if sex == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

daily_calories = bmr * activity_options[activity]

st.metric(
    "Daily Calories Needed",
    f"{round(daily_calories)} kcal"
)

st.markdown("---")

st.header("📈 Activity Level Comparison")

selected_levels = st.multiselect(
    "Select activity levels to compare",
    options=list(activity_options.keys())
)

if selected_levels:

    comparison_data = []

    for level in selected_levels:

        calories = round(
            bmr * activity_options[level]
        )

        comparison_data.append(
            {
                "Activity Level": level,
                "Multiplier": activity_options[level],
                "Calories Needed (kcal)": calories
            }
        )

    comparison_df = pd.DataFrame(comparison_data)

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

st.markdown("---")

st.header("🎯 Ideal Weight Range")

if sex == "Male":
    ideal_weight = (
        52 + 1.9 * ((height / 2.54) - 60)
    )
else:
    ideal_weight = (
        49 + 1.7 * ((height / 2.54) - 60)
    )

low_weight = ideal_weight * 0.9
high_weight = ideal_weight * 1.1

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Low Range",
        f"{low_weight:.1f} kg"
    )

with col2:
    st.metric(
        "High Range",
        f"{high_weight:.1f} kg"
    )

st.markdown("---")


st.header("📋 Full Summary")

if st.button("Show My Summary"):

    st.success("Summary Generated Successfully!")

    st.write(f"### Hello, {name}")

    st.write(f"**Age:** {age}")
    st.write(f"**Gender:** {sex}")
    st.write(f"**Weight:** {weight} kg")
    st.write(f"**Height:** {height} cm")

    st.metric(
        "BMI",
        round(bmi, 1)
    )

    st.write(
        f"**BMI Classification:** {bmi_category}"
    )

    st.write(
        f"**Health Risk:** {risk}"
    )

    st.metric(
        "Daily Calories Needed",
        f"{round(daily_calories)} kcal"
    )

    st.write(
        f"**Ideal Weight Range:** "
        f"{low_weight:.1f} kg - {high_weight:.1f} kg"
    )