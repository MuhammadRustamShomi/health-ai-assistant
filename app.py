import streamlit as st
import os
import math
import requests
from datetime import datetime, date

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthAI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a8a4a 0%, #0d5c8a 100%);
        padding: 1.5rem 2rem; border-radius: 12px;
        margin-bottom: 1.5rem; color: white; text-align: center;
    }
    .feature-card {
        background: #f8f9fa; border-left: 4px solid #1a8a4a;
        border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;
    }
    .metric-box {
        background: white; border: 1px solid #e0e0e0;
        border-radius: 10px; padding: 1rem; text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/medical-doctor.png", width=80)
    st.title("HealthAI 🏥")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Home", "💬 AI Health Chat", "🔍 Symptom Checker",
         "⚖️ BMI & Health Metrics", "😊 Mood Tracker", "🥗 Nutrition Guide"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**API Setup**")

    groq_key = st.text_input("Groq API Key (Free)", type="password",
                              placeholder="gsk_...", help="Get free key at console.groq.com")
    hf_token = st.text_input("HuggingFace Token (Free)", type="password",
                              placeholder="hf_...", help="Get free token at huggingface.co/settings/tokens")

    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
        st.success("✅ Groq connected")
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token
        st.success("✅ HuggingFace connected")

    st.markdown("---")
    st.caption("⚠️ For educational purposes only. Always consult a doctor.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 HealthAI Assistant</h1>
        <p>Your AI-Powered Personal Health Companion — Powered by Free LLMs & HuggingFace</p>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards = [
        ("💬", "AI Health Chat", "Ask health questions using Groq (Llama 3)"),
        ("🔍", "Symptom Checker", "NLP-based analysis via HuggingFace"),
        ("⚖️", "BMI & Metrics", "Calculate your health indicators"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3], cards):
        col.markdown(f"""<div class="metric-box"><h2>{icon}</h2><b>{title}</b><br><small>{desc}</small></div>""",
                     unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    cards2 = [
        ("😊", "Mood Tracker", "Track & analyze daily mental health"),
        ("🥗", "Nutrition Guide", "AI-powered diet recommendations"),
        ("🆓", "100% Free APIs", "Groq + HuggingFace free tiers"),
    ]
    for col, (icon, title, desc) in zip([col4, col5, col6], cards2):
        col.markdown(f"""<div class="metric-box"><h2>{icon}</h2><b>{title}</b><br><small>{desc}</small></div>""",
                     unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    <div class="feature-card">
    <b>Step 1:</b> Get your <a href="https://console.groq.com" target="_blank">free Groq API key</a> (No credit card needed)<br>
    <b>Step 2:</b> Get your <a href="https://huggingface.co/settings/tokens" target="_blank">free HuggingFace token</a><br>
    <b>Step 3:</b> Enter keys in the sidebar and start exploring!
    </div>""", unsafe_allow_html=True)

    with st.expander("📋 Disclaimer"):
        st.warning("This app is for **educational purposes only**. It does **not** replace professional medical advice.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI HEALTH CHAT
# ══════════════════════════════════════════════════════════════════════════════
CHAT_SYSTEM = """You are HealthAI, a knowledgeable and empathetic health assistant.
Provide clear, evidence-based health information. Always remind users to consult a
healthcare professional for diagnosis/treatment. Be supportive, never alarmist.
If asked about emergencies, immediately advise calling emergency services."""

def groq_chat(messages):
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": CHAT_SYSTEM}] + messages,
            max_tokens=1024, temperature=0.7,
        )
        return res.choices[0].message.content
    except ImportError:
        return "⚠️ Install groq: `pip install groq`"
    except Exception as e:
        return f"❌ Error: {e}\n\nCheck your Groq API key in the sidebar."

def page_chat():
    st.title("💬 AI Health Chat")
    st.caption("Powered by **Groq + Llama 3.3 70B** — completely free!")

    if not os.environ.get("GROQ_API_KEY"):
        st.warning("🔑 Enter your **Groq API Key** in the sidebar. Get it free at [console.groq.com](https://console.groq.com)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("**💡 Try asking:**")
    suggestions = ["What are common symptoms of dehydration?",
                   "How many hours of sleep do adults need?",
                   "Tips to reduce stress naturally",
                   "What foods boost the immune system?"]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        if cols[i % 2].button(s, key=f"sugg_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": s})
            reply = groq_chat(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("---")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🏥"):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a health question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🏥"):
            with st.spinner("Thinking..."):
                reply = groq_chat(st.session_state.chat_history)
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SYMPTOM CHECKER
# ══════════════════════════════════════════════════════════════════════════════
HF_ZSC_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

SYMPTOM_CATEGORIES = [
    "respiratory illness", "digestive problem", "cardiovascular issue",
    "neurological condition", "musculoskeletal pain", "skin condition",
    "mental health concern", "immune system issue", "hormonal imbalance",
    "nutritional deficiency",
]

CATEGORY_INFO = {
    "respiratory illness":   {"icon": "🫁", "advice": "Stay hydrated, rest, monitor breathing.", "doctor": "Difficulty breathing, chest pain, high fever, or symptoms > 7 days."},
    "digestive problem":     {"icon": "🫄", "advice": "Eat light (BRAT diet), stay hydrated, avoid fatty/spicy foods.", "doctor": "Blood in stool, severe abdominal pain, or symptoms > 48 hours."},
    "cardiovascular issue":  {"icon": "❤️", "advice": "Avoid strenuous activity, monitor blood pressure.", "doctor": "Chest pain or irregular heartbeat — seek IMMEDIATE care."},
    "neurological condition":{"icon": "🧠", "advice": "Rest, avoid screens, stay hydrated, minimize stress.", "doctor": "Sudden severe headache, vision changes, or confusion — emergency care."},
    "musculoskeletal pain":  {"icon": "🦴", "advice": "RICE: Rest, Ice, Compression, Elevation.", "doctor": "Severe pain, swelling, or inability to bear weight."},
    "skin condition":        {"icon": "🩹", "advice": "Keep skin clean and moisturized. Avoid scratching.", "doctor": "Rapidly spreading rash or signs of infection."},
    "mental health concern": {"icon": "😔", "advice": "Practice self-care: sleep, exercise, mindfulness.", "doctor": "Persistent sadness or thoughts of self-harm — seek help immediately."},
    "immune system issue":   {"icon": "🛡️", "advice": "Rest, eat immune-boosting foods, stay hydrated.", "doctor": "High fever, persistent fatigue, or recurring infections."},
    "hormonal imbalance":    {"icon": "⚗️", "advice": "Balanced diet, regular exercise, consistent sleep.", "doctor": "Unexplained weight changes or persistent mood swings."},
    "nutritional deficiency":{"icon": "🥗", "advice": "Eat varied diet: vegetables, fruits, whole grains, protein.", "doctor": "Extreme fatigue or hair loss persisting despite diet changes."},
}

def page_symptom_checker():
    st.title("🔍 Symptom Checker")
    st.caption("Uses **facebook/bart-large-mnli** (Zero-Shot Classification) from HuggingFace — Free!")

    if not os.environ.get("HF_TOKEN"):
        st.warning("🔑 Enter your **HuggingFace Token** in the sidebar. Get it free at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)")

    st.markdown("### Describe Your Symptoms")
    common = ["headache", "fever", "cough", "fatigue", "nausea",
              "chest pain", "shortness of breath", "dizziness", "rash", "muscle ache"]
    st.markdown("**🏷️ Common symptoms (click to add):**")
    selected = []
    chip_cols = st.columns(5)
    for i, s in enumerate(common):
        if chip_cols[i % 5].checkbox(s, key=f"chip_{i}"):
            selected.append(s)

    additional = st.text_area("Additional details:", placeholder="e.g., persistent headache for 2 days with light sensitivity...", height=100)

    full_input = ", ".join(selected)
    if additional.strip():
        full_input = f"{full_input}, {additional}" if full_input else additional

    if st.button("🔍 Analyze Symptoms", type="primary"):
        if not full_input.strip():
            st.error("Please select or describe symptoms first.")
            return
        token = os.environ.get("HF_TOKEN", "")
        if not token:
            st.error("HuggingFace token required.")
            return

        with st.spinner("🤖 Analyzing with AI..."):
            try:
                r = requests.post(HF_ZSC_URL,
                                  headers={"Authorization": f"Bearer {token}"},
                                  json={"inputs": full_input, "parameters": {"candidate_labels": SYMPTOM_CATEGORIES}},
                                  timeout=30)
                result = r.json()

                if "error" in result:
                    st.error(f"API Error: {result['error']} — Model may be loading, try again in 20s.")
                    return

                labels, scores = result.get("labels", []), result.get("scores", [])
                st.markdown("---")
                st.markdown("### 📊 Analysis Results")
                for i in range(min(3, len(labels))):
                    cat, score = labels[i], scores[i]
                    info = CATEGORY_INFO.get(cat, {})
                    with st.expander(f"{info.get('icon','🔵')} **{cat.title()}** — Confidence: {score:.0%}", expanded=(i == 0)):
                        st.progress(score)
                        st.markdown(f"**💡 Self-care:** {info.get('advice', 'Consult a provider.')}")
                        st.markdown(f"**🚨 See a doctor if:** {info.get('doctor', 'Symptoms persist or worsen.')}")

                st.error("⚠️ This is AI analysis for educational purposes only — NOT a medical diagnosis.")

            except requests.exceptions.Timeout:
                st.error("Timeout. The model may be loading. Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BMI & HEALTH METRICS
# ══════════════════════════════════════════════════════════════════════════════
def page_bmi():
    st.title("⚖️ BMI & Health Metrics")
    st.caption("Calculate your key health indicators instantly")

    tab1, tab2, tab3 = st.tabs(["📏 BMI Calculator", "🔥 Calorie Needs (TDEE)", "💧 Water Intake"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            unit = st.radio("Unit", ["Metric (kg/cm)", "Imperial (lbs/ft-in)"], horizontal=True)
        with col2:
            age = st.number_input("Age", 1, 120, 25)

        if unit == "Metric (kg/cm)":
            weight = st.slider("Weight (kg)", 30.0, 200.0, 70.0, 0.5)
            height = st.slider("Height (cm)", 100.0, 230.0, 170.0, 0.5)
        else:
            lbs = st.slider("Weight (lbs)", 66.0, 440.0, 154.0, 1.0)
            ft = st.slider("Height (feet)", 4, 7, 5)
            inches = st.slider("Height (inches)", 0, 11, 7)
            weight = lbs * 0.453592
            height = (ft * 12 + inches) * 2.54

        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5: cat, color = "Underweight 🔵", "#3498db"
        elif bmi < 25: cat, color = "Normal Weight 🟢", "#27ae60"
        elif bmi < 30: cat, color = "Overweight 🟡", "#f39c12"
        else:          cat, color = "Obese 🔴", "#e74c3c"

        h_m = height / 100
        ideal_low, ideal_high = round(18.5 * h_m**2, 1), round(24.9 * h_m**2, 1)

        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("BMI", f"{bmi:.1f}")
        m2.metric("Category", cat)
        m3.metric("Ideal Weight", f"{ideal_low}–{ideal_high} kg")

        prog = max(0.0, min(1.0, (bmi - 15) / 25))
        st.markdown(f"""
        <div style="background:#eee;border-radius:10px;height:20px;overflow:hidden;margin-top:1rem;">
          <div style="width:{prog*100:.0f}%;background:{color};height:100%;border-radius:10px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#888;margin-top:4px;">
          <span>&lt;18.5 Underweight</span><span>18.5–24.9 Normal</span><span>25–29.9 Overweight</span><span>30+ Obese</span>
        </div>""", unsafe_allow_html=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            tw = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, key="tw")
            th = st.number_input("Height (cm)", 100.0, 230.0, 170.0, key="th")
        with c2:
            ta = st.number_input("Age", 1, 100, 25, key="ta")
            tg = st.radio("Gender", ["Male", "Female"], key="tg")

        activity_map = {
            "Sedentary (little/no exercise)": 1.2,
            "Light (1–3 days/week)": 1.375,
            "Moderate (3–5 days/week)": 1.55,
            "Active (6–7 days/week)": 1.725,
            "Very Active (hard exercise + physical job)": 1.9,
        }
        act = st.selectbox("Activity Level", list(activity_map.keys()))
        bmr = (10*tw + 6.25*th - 5*ta + 5) if tg == "Male" else (10*tw + 6.25*th - 5*ta - 161)
        tdee = bmr * activity_map[act]

        st.markdown("---")
        r1, r2, r3 = st.columns(3)
        r1.metric("BMR", f"{bmr:.0f} kcal/day")
        r2.metric("TDEE (Maintain)", f"{tdee:.0f} kcal/day")
        r3.metric("Weight Loss Target", f"{tdee-500:.0f} kcal/day")
        st.info(f"💡 To gain weight, aim for ~{tdee+300:.0f} kcal/day.")

    with tab3:
        ww = st.slider("Weight (kg)", 30, 150, 70, key="ww")
        wa = st.radio("Activity", ["Low", "Moderate", "High"], horizontal=True)
        wc = st.radio("Climate", ["Temperate", "Hot/Humid"], horizontal=True)
        water = ww * 35
        if wa == "Moderate": water += 400
        elif wa == "High": water += 700
        if wc == "Hot/Humid": water += 500
        water /= 1000
        glasses = math.ceil(water / 0.25)
        wa1, wa2 = st.columns(2)
        wa1.metric("Daily Water", f"{water:.1f} L")
        wa2.metric("Glasses (250ml)", f"{glasses}")
        st.progress(min(1.0, water / 4))
        st.success(f"💧 Aim for {water:.1f} litres ({glasses} glasses) daily.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MOOD TRACKER
# ══════════════════════════════════════════════════════════════════════════════
HF_EMOTION_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
MOOD_EMOJIS = {1: "😢", 2: "😟", 3: "😐", 4: "🙂", 5: "😄"}
MOOD_LABELS = {1: "Very Low", 2: "Low", 3: "Neutral", 4: "Good", 5: "Excellent"}

def page_mood():
    st.title("😊 Mood Tracker")
    st.caption("Track mental wellness with **AI emotion analysis** — HuggingFace Free Models")

    if "mood_entries" not in st.session_state:
        st.session_state.mood_entries = []

    tab1, tab2 = st.tabs(["📝 Log Mood", "📊 My History"])

    with tab1:
        st.markdown("### How are you feeling today?")
        mood_score = st.select_slider("Mood Level", options=[1,2,3,4,5], value=3,
                                      format_func=lambda x: f"{MOOD_EMOJIS[x]} {MOOD_LABELS[x]}")
        journal = st.text_area("📓 Journal Entry (optional):",
                               placeholder="Write how you're feeling...", height=120)
        factors = st.multiselect("Contributing factors:",
                                 ["Sleep","Exercise","Diet","Work stress","Social connection",
                                  "Weather","Health","Personal achievement","Relationships"])

        if st.button("💾 Save Entry", type="primary"):
            entry = {
                "date": date.today().isoformat(),
                "time": datetime.now().strftime("%H:%M"),
                "mood_score": mood_score,
                "mood_label": MOOD_LABELS[mood_score],
                "emoji": MOOD_EMOJIS[mood_score],
                "journal": journal,
                "factors": factors,
                "emotions": [],
            }
            token = os.environ.get("HF_TOKEN", "")
            if journal.strip() and token:
                with st.spinner("Analyzing emotions..."):
                    try:
                        r = requests.post(HF_EMOTION_URL,
                                          headers={"Authorization": f"Bearer {token}"},
                                          json={"inputs": journal}, timeout=30)
                        result = r.json()
                        if isinstance(result, list) and result:
                            emotions = result[0] if isinstance(result[0], list) else result
                            entry["emotions"] = sorted(emotions, key=lambda x: x.get("score",0), reverse=True)[:3]
                    except Exception:
                        pass

            st.session_state.mood_entries.append(entry)
            st.success(f"✅ Entry saved for {entry['date']} at {entry['time']}")

            if entry["emotions"]:
                st.markdown("**🧠 Detected Emotions:**")
                for emo in entry["emotions"]:
                    st.progress(emo.get("score", 0), text=f"{emo.get('label','').title()}: {emo.get('score',0):.0%}")

            tips = {
                1: "🌱 Be gentle with yourself. Reach out to someone you trust.",
                2: "🌿 Try a 10-minute walk outside — fresh air shifts your mood.",
                3: "☀️ Stick to your routine: meals, hydration, sleep.",
                4: "✨ Use this energy for something creative or social!",
                5: "🎉 Wonderful! Journal what made today great.",
            }
            st.info(tips[mood_score])
            if mood_score <= 2:
                st.error("If you're struggling: **Crisis Text Line** — Text HOME to 741741")

    with tab2:
        if not st.session_state.mood_entries:
            st.info("No entries yet. Log your first mood!")
            return

        entries = st.session_state.mood_entries
        avg = sum(e["mood_score"] for e in entries) / len(entries)
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Entries", len(entries))
        s2.metric("Average Mood", f"{MOOD_EMOJIS[round(avg)]} {avg:.1f}/5")
        s3.metric("Latest", f"{entries[-1]['emoji']} {entries[-1]['mood_label']}")

        st.markdown("---")
        st.markdown("**📈 Mood Trend:**")
        import pandas as pd
        df = pd.DataFrame([{"Time": f"{e['date']} {e['time']}", "Mood": e["mood_score"]} for e in entries])
        st.line_chart(df.set_index("Time"))

        st.markdown("---")
        for e in reversed(entries[-10:]):
            with st.expander(f"{e['emoji']} {e['date']} {e['time']} — {e['mood_label']}"):
                if e["journal"]: st.markdown(f"*{e['journal']}*")
                if e["factors"]: st.markdown(f"**Factors:** {', '.join(e['factors'])}")
                for emo in e.get("emotions", []):
                    st.caption(f"• {emo.get('label','').title()}: {emo.get('score',0):.0%}")

        if st.button("🗑️ Clear History"):
            st.session_state.mood_entries = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: NUTRITION GUIDE
# ══════════════════════════════════════════════════════════════════════════════
NUTRITION_SYSTEM = """You are NutriAI, a knowledgeable nutrition assistant.
Provide science-backed dietary advice. Create practical, realistic meal plans.
Use emojis to make responses engaging. Format meal plans clearly with sections.
Always remind that a registered dietitian can provide personalized guidance."""

FOOD_NUTRIENTS = {
    "Banana":        {"calories": 89,  "protein": 1.1, "carbs": 23,  "fat": 0.3,  "fiber": 2.6},
    "Chicken Breast":{"calories": 165, "protein": 31,  "carbs": 0,   "fat": 3.6,  "fiber": 0},
    "Brown Rice":    {"calories": 216, "protein": 5,   "carbs": 45,  "fat": 1.8,  "fiber": 3.5},
    "Broccoli":      {"calories": 55,  "protein": 3.7, "carbs": 11,  "fat": 0.6,  "fiber": 5.1},
    "Egg":           {"calories": 155, "protein": 13,  "carbs": 1.1, "fat": 11,   "fiber": 0},
    "Salmon":        {"calories": 208, "protein": 20,  "carbs": 0,   "fat": 13,   "fiber": 0},
    "Oats":          {"calories": 389, "protein": 17,  "carbs": 66,  "fat": 7,    "fiber": 11},
    "Greek Yogurt":  {"calories": 100, "protein": 10,  "carbs": 3.6, "fat": 5,    "fiber": 0},
    "Almonds":       {"calories": 579, "protein": 21,  "carbs": 22,  "fat": 50,   "fiber": 12.5},
    "Sweet Potato":  {"calories": 86,  "protein": 1.6, "carbs": 20,  "fat": 0.1,  "fiber": 3},
}

def page_nutrition():
    st.title("🥗 Nutrition Guide")
    st.caption("AI-powered nutrition with **Groq Llama 3** + food nutrient lookup")

    if not os.environ.get("GROQ_API_KEY"):
        st.warning("🔑 Enter your **Groq API Key** in the sidebar. Get free at [console.groq.com](https://console.groq.com)")

    tab1, tab2, tab3 = st.tabs(["🤖 AI Meal Planner", "🔎 Food Lookup", "📋 Quick Tips"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            goal = st.selectbox("Your Goal", ["Weight Loss","Muscle Gain","Maintain Weight",
                                              "Improve Energy","Heart Health","Manage Diabetes"])
            calories = st.number_input("Daily Calorie Target", 1000, 4000, 2000, 100)
        with c2:
            diet = st.selectbox("Diet Preference", ["No preference","Vegetarian","Vegan",
                                                     "Keto","Mediterranean","Gluten-Free","Dairy-Free"])
            allergies = st.multiselect("Allergies/Avoid:", ["Nuts","Dairy","Gluten","Eggs","Seafood","Soy"])

        notes = st.text_input("Special notes:", placeholder="e.g., I eat dinner late")

        if st.button("🍽️ Generate Meal Plan", type="primary"):
            allergy_str = f"Avoid: {', '.join(allergies)}." if allergies else ""
            prompt = (f"Create a detailed 1-day meal plan. Goal: {goal}. "
                      f"Calories: {calories} kcal. Diet: {diet}. {allergy_str} {notes} "
                      f"Include breakfast, lunch, dinner, 2 snacks with portions. "
                      f"End with 3 practical tips.")
            with st.spinner("🤖 Creating your meal plan..."):
                try:
                    from groq import Groq
                    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"system","content":NUTRITION_SYSTEM},
                                  {"role":"user","content":prompt}],
                        max_tokens=1500, temperature=0.6,
                    )
                    plan = res.choices[0].message.content
                except ImportError:
                    plan = "⚠️ Install groq: `pip install groq`"
                except Exception as e:
                    plan = f"❌ Error: {e}"
            st.markdown("---")
            st.markdown("### 📋 Your Personalized Meal Plan")
            st.markdown(plan)

    with tab2:
        selected_foods = st.multiselect("Select foods to compare:", list(FOOD_NUTRIENTS.keys()))
        if selected_foods:
            import pandas as pd
            df = pd.DataFrame([{"Food": f, **FOOD_NUTRIENTS[f]} for f in selected_foods])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.bar_chart(df.set_index("Food")["calories"])
        else:
            st.info("Select foods above to see their nutritional data (per 100g).")

    with tab3:
        tips = {
            "🥦 Eat the Rainbow": "Aim for 5–9 servings of colorful fruits and vegetables daily.",
            "💧 Hydrate Before Hunger": "Dehydration often mimics hunger. Drink water first.",
            "🥚 Protein at Every Meal": "Protein increases satiety and preserves muscle mass.",
            "🌾 Choose Whole Grains": "Improve fiber intake and blood sugar control.",
            "🥑 Healthy Fats Are Essential": "Avocado, nuts, olive oil support brain and hormone health.",
            "⏰ Mindful Eating": "Eat slowly — it takes 20 mins for your brain to register fullness.",
            "🍽️ Plate Method": "½ vegetables, ¼ lean protein, ¼ whole grains per meal.",
            "🚫 Limit Ultra-Processed Foods": "Long ingredient lists + added sugars = chronic disease risk.",
        }
        cols = st.columns(2)
        for i, (title, tip) in enumerate(tips.items()):
            cols[i % 2].markdown(f"""<div class="feature-card"><b>{title}</b><br><small>{tip}</small></div>""",
                                  unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if   page == "🏠 Home":               page_home()
elif page == "💬 AI Health Chat":     page_chat()
elif page == "🔍 Symptom Checker":    page_symptom_checker()
elif page == "⚖️ BMI & Health Metrics": page_bmi()
elif page == "😊 Mood Tracker":       page_mood()
elif page == "🥗 Nutrition Guide":    page_nutrition()
