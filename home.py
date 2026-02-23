import streamlit as st

def show():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 HealthAI Assistant</h1>
        <p>Your AI-Powered Personal Health Companion — Powered by Free LLMs & HuggingFace</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-box">
        <h2>💬</h2><b>AI Health Chat</b><br>
        <small>Ask health questions using Groq (Llama 3)</small></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-box">
        <h2>🔍</h2><b>Symptom Checker</b><br>
        <small>NLP-based analysis via HuggingFace</small></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-box">
        <h2>⚖️</h2><b>BMI & Metrics</b><br>
        <small>Calculate your health indicators</small></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("""<div class="metric-box">
        <h2>😊</h2><b>Mood Tracker</b><br>
        <small>Track & analyze daily mental health</small></div>""", unsafe_allow_html=True)
    with col5:
        st.markdown("""<div class="metric-box">
        <h2>🥗</h2><b>Nutrition Guide</b><br>
        <small>AI-powered diet recommendations</small></div>""", unsafe_allow_html=True)
    with col6:
        st.markdown("""<div class="metric-box">
        <h2>🆓</h2><b>100% Free APIs</b><br>
        <small>Groq + HuggingFace free tiers</small></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    <div class="feature-card">
    <b>Step 1:</b> Get your <a href="https://console.groq.com" target="_blank">free Groq API key</a> (Llama 3 — No credit card needed)<br>
    <b>Step 2:</b> Get your <a href="https://huggingface.co/settings/tokens" target="_blank">free HuggingFace token</a> (Inference API)<br>
    <b>Step 3:</b> Enter keys in the sidebar and start exploring!
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📋 Disclaimer"):
        st.warning("This app is built for **educational purposes only**. It does **not** replace professional medical advice. Always consult a qualified healthcare provider for medical concerns.")
