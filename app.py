import streamlit as st
import os

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
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .feature-card {
        background: #f8f9fa;
        border-left: 4px solid #1a8a4a;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .stAlert { border-radius: 8px; }
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

    groq_key = st.text_input(
        "Groq API Key (Free)",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com",
    )
    hf_token = st.text_input(
        "HuggingFace Token (Free)",
        type="password",
        placeholder="hf_...",
        help="Get your free token at huggingface.co/settings/tokens",
    )

    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
        st.success("✅ Groq connected")
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token
        st.success("✅ HuggingFace connected")

    st.markdown("---")
    st.caption("⚠️ For educational purposes only. Always consult a doctor.")

# ── Pages ──────────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    from modules.home import show
    show()
elif page == "💬 AI Health Chat":
    from modules.chat import show
    show()
elif page == "🔍 Symptom Checker":
    from modules.symptom_checker import show
    show()
elif page == "⚖️ BMI & Health Metrics":
    from modules.bmi import show
    show()
elif page == "😊 Mood Tracker":
    from modules.mood import show
    show()
elif page == "🥗 Nutrition Guide":
    from modules.nutrition import show
    show()
