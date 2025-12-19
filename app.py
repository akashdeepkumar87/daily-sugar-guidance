import streamlit as st
import os
from datetime import datetime
import pandas as pd

# -------------------------------------------------
# App Configuration
# -------------------------------------------------
st.set_page_config(page_title="Daily Sugar Guidance", layout="centered")

# -------------------------------------------------
# File Path Setup
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "sugar_history.csv")

# -------------------------------------------------
# Save Sugar History
# -------------------------------------------------
def save_sugar_history(sugar_value):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = pd.DataFrame({
        "datetime": [timestamp],
        "sugar": [sugar_value]
    })

    if os.path.exists(CSV_PATH):
        old_data = pd.read_csv(CSV_PATH)
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
        updated_data.to_csv(CSV_PATH, index=False)
    else:
        new_data.to_csv(CSV_PATH, index=False)


# -------------------------------------------------
# Smart Insight Logic
# -------------------------------------------------
def get_smart_insight():
    if not os.path.exists(CSV_PATH):
        return "No history available yet."

    data = pd.read_csv(CSV_PATH)

    if len(data) < 2:
        return "This is your first entry. Add more daily values to see comparisons."

    today_value = data.iloc[-1]["sugar"]
    yesterday_value = data.iloc[-2]["sugar"]

    if today_value < yesterday_value:
        return f"Good progress. Today's sugar is lower than yesterday by {int(yesterday_value - today_value)} mg/dL."
    elif today_value > yesterday_value:
        return f"Attention needed. Today's sugar is higher than yesterday by {int(today_value - yesterday_value)} mg/dL."
    else:
        return "Your sugar level is the same as yesterday. Maintain your routine."

# -------------------------------------------------
# Sugar Trend Graph
# -------------------------------------------------
import matplotlib.pyplot as plt

def show_sugar_trend():
    if not os.path.exists(CSV_PATH):
        st.info("No data available to show trends.")
        return

    data = pd.read_csv(CSV_PATH)

    if len(data) < 2:
        st.info("Add more daily entries to see your sugar trend.")
        return

    recent_data = data.tail(7)

    # Color coding based on sugar level
    colors = []
    for val in recent_data["sugar"]:
        if val < 70:
            colors.append("red")
        elif 70 <= val <= 100:
            colors.append("green")
        elif 100 < val <= 125:
            colors.append("orange")
        else:
            colors.append("red")

    fig, ax = plt.subplots()

    ax.bar(
        range(len(recent_data)),
        recent_data["sugar"],
        color=colors
    )

    ax.axhspan(70, 100, alpha=0.2)
    ax.text(0, 102, "Normal Range (70–100 mg/dL)", fontsize=9)

    ax.set_title("Blood Sugar Levels (Last 7 Entries)")
    ax.set_xlabel("Recent Entries")
    ax.set_ylabel("Sugar Level (mg/dL)")

    ax.set_xticks(range(len(recent_data)))
    ax.set_xticklabels(recent_data["datetime"], rotation=45)

    plt.tight_layout()
    st.pyplot(fig)



# -------------------------------------------------
# Sugar Trend (On Button Click)
# -------------------------------------------------
show_trend = st.toggle("📊 Show Sugar Trend (Last 7 Entries)")

if show_trend:
    show_sugar_trend()


# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🩺 Daily Sugar Guidance")
st.write(
    "Enter your **morning blood sugar level** and press **Enter** or click the button "
    "to receive guidance for today."
)

# -------------------------------------------------
# Input Form
# -------------------------------------------------
with st.form("sugar_form"):
    sugar = st.number_input(
        "Morning Blood Sugar (mg/dL)",
        min_value=0,
        max_value=600,
        step=1,
        help="Example: 85, 110, 165"
    )
    submit = st.form_submit_button("Get Today's Guidance")

# -------------------------------------------------
# Application Logic
# -------------------------------------------------
if submit:

    if sugar <= 0:
        st.error("Invalid input")
        st.write("Blood sugar must be a positive value.")
        st.stop()

    save_sugar_history(sugar)

    # Emergency conditions
    if sugar < 40:
        st.error("Critical Low Blood Sugar")
        st.write("Take a fast-acting sugar source immediately and seek medical help.")
        st.stop()

    if sugar > 400:
        st.error("Extremely High Blood Sugar")
        st.write("Seek medical attention immediately.")
        st.stop()

    # Normal ranges
    if sugar < 70:
        status = "LOW"
        color = "🔴"
        meaning = "Your blood sugar is below the normal range."
        diet_yes = ["Take a quick sugar source such as juice or glucose."]
        diet_no = []
        activity = "Avoid physical activity."
        focus = "Restore blood sugar safely."

    elif 70 <= sugar <= 100:
        status = "NORMAL"
        color = "🟢"
        meaning = "Your blood sugar is within the healthy normal range."
        diet_yes = ["Continue balanced home-cooked meals."]
        diet_no = ["Avoid excess sugar."]
        activity = "15–20 minutes of light walking."
        focus = "Maintain a healthy routine."

    elif 100 < sugar <= 125:
        status = "BORDERLINE"
        color = "🟡"
        meaning = "Your blood sugar is slightly above normal."
        diet_yes = ["Prefer light meals."]
        diet_no = ["Reduce sugar and refined carbohydrates."]
        activity = "20 minutes of walking."
        focus = "Improve sugar control."

    else:
        status = "HIGH"
        color = "🔴"
        meaning = "Your blood sugar is high today."
        diet_yes = ["Eat light, home-cooked meals."]
        diet_no = ["Avoid sweets, sugary drinks, and high-carb foods."]
        activity = "25–30 minutes of light to moderate walking."
        focus = "Reduce sugar levels safely."

    # -------------------------------------------------
    # Output
    # -------------------------------------------------
    st.markdown(f"## {color} Sugar Status: **{status}**")
    st.markdown(f"### 🔢 Blood Sugar: **{sugar} mg/dL**")

    st.subheader("What This Means")
    st.write(meaning)

    st.subheader("Diet Recommendation")
    for item in diet_yes:
        st.write("✔", item)
    for item in diet_no:
        st.write("✖", item)

    st.subheader("Physical Activity")
    st.write(activity)

    st.subheader("Today's Focus")
    st.success(focus)

   
