import streamlit as st
import math

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def bmi_category(bmi: float) -> tuple:
    if bmi < 18.5:
        return "Underweight", "🔵", "#3498db"
    elif bmi < 25:
        return "Normal Weight", "🟢", "#27ae60"
    elif bmi < 30:
        return "Overweight", "🟡", "#f39c12"
    else:
        return "Obese", "🔴", "#e74c3c"

def ideal_weight_range(height_cm: float) -> tuple:
    height_m = height_cm / 100
    low = 18.5 * (height_m ** 2)
    high = 24.9 * (height_m ** 2)
    return round(low, 1), round(high, 1)

def calculate_bmr(weight_kg, height_cm, age, gender):
    """Mifflin-St Jeor Equation"""
    if gender == "Male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

ACTIVITY_MULTIPLIERS = {
    "Sedentary (little/no exercise)": 1.2,
    "Light (1–3 days/week)": 1.375,
    "Moderate (3–5 days/week)": 1.55,
    "Active (6–7 days/week)": 1.725,
    "Very Active (hard exercise + physical job)": 1.9,
}

def show():
    st.title("⚖️ BMI & Health Metrics")
    st.caption("Calculate your key health indicators instantly")

    tab1, tab2, tab3 = st.tabs(["📏 BMI Calculator", "🔥 Calorie Needs (TDEE)", "💧 Water Intake"])

    # ── TAB 1: BMI ──────────────────────────────────────────────────────────────
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            unit = st.radio("Unit system", ["Metric (kg/cm)", "Imperial (lbs/ft-in)"], horizontal=True)
        with col2:
            age = st.number_input("Age", min_value=1, max_value=120, value=25)

        if unit == "Metric (kg/cm)":
            weight = st.slider("Weight (kg)", 30.0, 200.0, 70.0, 0.5)
            height = st.slider("Height (cm)", 100.0, 230.0, 170.0, 0.5)
        else:
            lbs = st.slider("Weight (lbs)", 66.0, 440.0, 154.0, 1.0)
            ft = st.slider("Height (feet)", 4, 7, 5)
            inches = st.slider("Height (inches)", 0, 11, 7)
            weight = lbs * 0.453592
            height = (ft * 12 + inches) * 2.54

        bmi = calculate_bmi(weight, height)
        cat, icon, color = bmi_category(bmi)
        low, high = ideal_weight_range(height)

        st.markdown("---")
        st.markdown("### Your Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("BMI", f"{bmi:.1f}")
        m2.metric("Category", f"{icon} {cat}")
        m3.metric("Ideal Weight Range", f"{low}–{high} kg")

        # Visual gauge
        bmi_clamped = max(15, min(bmi, 40))
        progress = (bmi_clamped - 15) / 25
        st.markdown(f"""
        <div style="background:#eee; border-radius:10px; height:20px; overflow:hidden; margin-top:1rem;">
          <div style="width:{progress*100:.0f}%; background:{color}; height:100%; border-radius:10px; transition:width 0.5s;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#888; margin-top:4px;">
          <span>Underweight &lt;18.5</span><span>Normal 18.5–24.9</span><span>Overweight 25–29.9</span><span>Obese 30+</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if cat == "Normal Weight":
            st.success("✅ Your BMI is in the healthy range. Maintain a balanced diet and regular exercise!")
        elif cat == "Underweight":
            st.info("ℹ️ Consider a nutrient-rich diet. Consult a dietitian for personalized guidance.")
        elif cat == "Overweight":
            st.warning("⚠️ Lifestyle changes (diet + exercise) can help. Consider consulting a healthcare provider.")
        else:
            st.error("🔴 Obesity increases health risks. Please consult a healthcare professional for support.")

    # ── TAB 2: TDEE ────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("### Daily Calorie Needs (TDEE)")
        c1, c2 = st.columns(2)
        with c1:
            td_weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="td_w")
            td_height = st.number_input("Height (cm)", 100.0, 230.0, 170.0, key="td_h")
        with c2:
            td_age = st.number_input("Age", 1, 100, 25, key="td_age")
            td_gender = st.radio("Gender", ["Male", "Female"], key="td_g")

        activity = st.selectbox("Activity Level", list(ACTIVITY_MULTIPLIERS.keys()))

        bmr = calculate_bmr(td_weight, td_height, td_age, td_gender)
        tdee = bmr * ACTIVITY_MULTIPLIERS[activity]

        st.markdown("---")
        r1, r2, r3 = st.columns(3)
        r1.metric("BMR (Base)", f"{bmr:.0f} kcal/day", help="Calories burned at complete rest")
        r2.metric("TDEE (Maintain)", f"{tdee:.0f} kcal/day", help="Total daily energy expenditure")
        r3.metric("For Weight Loss", f"{tdee - 500:.0f} kcal/day", help="500 kcal deficit = ~0.5kg/week loss")

        st.info(f"💡 To **gain weight**, aim for ~{tdee + 300:.0f} kcal/day (+300 surplus).")

    # ── TAB 3: Water ───────────────────────────────────────────────────────────
    with tab3:
        st.markdown("### Daily Water Intake Calculator")
        w_weight = st.slider("Your weight (kg)", 30, 150, 70, key="w_w")
        w_activity = st.radio("Activity level", ["Low", "Moderate", "High"], horizontal=True)
        w_climate = st.radio("Climate", ["Temperate", "Hot/Humid"], horizontal=True)

        base_water = w_weight * 35  # ml
        if w_activity == "Moderate":
            base_water += 400
        elif w_activity == "High":
            base_water += 700
        if w_climate == "Hot/Humid":
            base_water += 500

        base_water /= 1000  # litres
        glasses = math.ceil(base_water / 0.25)

        st.markdown("---")
        wa, wb = st.columns(2)
        wa.metric("Daily Water Intake", f"{base_water:.1f} L")
        wb.metric("Equivalent Glasses (250ml)", f"{glasses} glasses")

        st.progress(min(1.0, base_water / 4))
        st.success(f"💧 Aim to drink **{base_water:.1f} litres** ({glasses} glasses) of water daily.")
