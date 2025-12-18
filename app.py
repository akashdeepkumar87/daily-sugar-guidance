import streamlit as st

st.set_page_config(page_title="Daily Sugar Guidance", layout="centered")

st.title("🩺 Daily Sugar Guidance")
st.write(
    "Enter your **morning blood sugar level** and press **Enter** or click the button "
    "to get guidance for today."
)

# -------- FORM START --------
with st.form(key="sugar_form"):
    sugar = st.number_input(
        "Morning Blood Sugar (mg/dL)",
        min_value=0,
        max_value=600,
        step=1,
        help="Example: 85, 110, 165"
    )
    submit = st.form_submit_button("Get Today’s Guidance")

# -------- LOGIC --------
if submit:

    # ❌ Invalid input
    if sugar <= 0:
        st.error("❌ Invalid input")
        st.write("👉 Sugar zero ya negative nahi hoti. Sahi number daalo.")

    # 🚨 Critical low
    elif sugar < 40:
        st.error("🚨 Critical Low Blood Sugar")
        st.markdown(f"### 🔴 Sugar: **{sugar} mg/dL**")
        st.markdown("### ✅ Turant kya karo")
        st.write("🧃 Juice / glucose lo")
        st.write("🏥 Doctor ke paas turant jao")
        st.write("❌ Walk mat karo")

    # 🚨 Extreme high
    elif sugar > 400:
        st.error("🚨 Extremely High Blood Sugar")
        st.markdown(f"### 🔴 Sugar: **{sugar} mg/dL**")
        st.markdown("### ⚠️ Important")
        st.write("🏥 Doctor ko turant dikhao")
        st.write("❌ Walk mat karo")

    # ✅ Normal flow
    else:
        # ---------- SAME LOGIC ----------
        if sugar < 70:
            status = "LOW"
            color = "🔴"
            meaning = "Your blood sugar is lower than the normal range and needs quick attention."
            diet_yes = [
                "🧃 Take a quick sugar source (juice, glucose, or candy)"
            ]
            diet_no = []
            activity = "❌ Avoid exercise. Rest and monitor your sugar."
            focus = "Sugar recovery and safety"

        elif 70 <= sugar <= 100:
            status = "NORMAL"
            color = "🟢"
            meaning = "Your blood sugar is within the healthy normal range."
            diet_yes = [
                "🍛 Continue balanced home-cooked food"
            ]
            diet_no = [
                "🍬 Avoid overeating and excess sugar"
            ]
            activity = "🚶 15–20 minutes of light walking"
            focus = "Maintain your routine"

        elif 100 < sugar <= 125:
            status = "BORDERLINE"
            color = "🟡"
            meaning = "Your blood sugar is slightly higher than normal and needs control."
            diet_yes = [
                "🥗 Prefer light meals"
            ]
            diet_no = [
                "🍚 Reduce sugar and refined carbohydrates"
            ]
            activity = "🚶 20 minutes of walking"
            focus = "Diet control with activity"

        else:
            status = "HIGH"
            color = "🔴"
            meaning = "Your blood sugar is high today and needs attention."
            diet_yes = [
                "🥗 Prefer light, home-cooked meals"
            ]
            diet_no = [
                "🍬 Avoid sweets, sugary drinks, and high-carb food"
            ]
            activity = "🚶 25–30 minutes of light to moderate walking"
            focus = "Reducing sugar levels"

        # -------- OUTPUT (VISUAL + SAME TEXT) --------
        st.markdown(f"## {color} Sugar Status: **{status}**")
        st.markdown(f"### 🔢 Blood Sugar: **{sugar} mg/dL**")

        st.subheader("📌 What This Means")
        st.write(meaning)

        st.subheader("🍽️ What to Eat Today")
        for item in diet_yes:
            st.write("✅", item)
        for item in diet_no:
            st.write("❌", item)

        st.subheader("🏃 What Activity to Do")
        st.write(activity)

        st.subheader("🎯 Today’s Focus")
        st.success(focus)

        st.info(
            "⚠️ This app provides general guidance only and does not replace medical advice."
        )
