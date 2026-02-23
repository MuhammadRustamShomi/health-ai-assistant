import streamlit as st
import os
import requests

# HuggingFace free zero-shot classification model
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

SYMPTOM_CATEGORIES = [
    "respiratory illness",
    "digestive problem",
    "cardiovascular issue",
    "neurological condition",
    "musculoskeletal pain",
    "skin condition",
    "mental health concern",
    "immune system issue",
    "hormonal imbalance",
    "nutritional deficiency",
]

CATEGORY_INFO = {
    "respiratory illness": {
        "icon": "🫁",
        "advice": "Stay hydrated, rest, and monitor breathing. See a doctor if breathing becomes difficult.",
        "when_to_see_doctor": "Difficulty breathing, chest pain, high fever, or symptoms lasting > 7 days.",
    },
    "digestive problem": {
        "icon": "🫄",
        "advice": "Eat light foods (BRAT diet), stay hydrated, and avoid fatty/spicy foods.",
        "when_to_see_doctor": "Blood in stool, severe abdominal pain, dehydration, or symptoms > 48 hours.",
    },
    "cardiovascular issue": {
        "icon": "❤️",
        "advice": "Avoid strenuous activity, monitor blood pressure, reduce salt and saturated fats.",
        "when_to_see_doctor": "Chest pain, shortness of breath, or irregular heartbeat — seek IMMEDIATE care.",
    },
    "neurological condition": {
        "icon": "🧠",
        "advice": "Rest, avoid screens, stay hydrated, and minimize stress.",
        "when_to_see_doctor": "Sudden severe headache, vision changes, numbness, or confusion — seek emergency care.",
    },
    "musculoskeletal pain": {
        "icon": "🦴",
        "advice": "RICE method: Rest, Ice, Compression, Elevation. Gentle stretching may help.",
        "when_to_see_doctor": "Severe pain, swelling, inability to bear weight, or pain after injury.",
    },
    "skin condition": {
        "icon": "🩹",
        "advice": "Keep skin clean and moisturized. Avoid scratching or irritants.",
        "when_to_see_doctor": "Rapidly spreading rash, signs of infection, or severe allergic reaction.",
    },
    "mental health concern": {
        "icon": "😔",
        "advice": "Practice self-care: sleep, exercise, mindfulness. Reach out to trusted people.",
        "when_to_see_doctor": "Persistent sadness, anxiety interfering with daily life, or thoughts of self-harm.",
    },
    "immune system issue": {
        "icon": "🛡️",
        "advice": "Rest, eat immune-boosting foods (vitamin C, zinc), and stay hydrated.",
        "when_to_see_doctor": "High fever, persistent fatigue, or recurring infections.",
    },
    "hormonal imbalance": {
        "icon": "⚗️",
        "advice": "Maintain a balanced diet, regular exercise, and consistent sleep schedule.",
        "when_to_see_doctor": "Unexplained weight changes, fatigue, or mood swings — consult an endocrinologist.",
    },
    "nutritional deficiency": {
        "icon": "🥗",
        "advice": "Eat a varied, balanced diet rich in vegetables, fruits, whole grains, and lean proteins.",
        "when_to_see_doctor": "Extreme fatigue, hair loss, or symptoms persisting despite dietary changes.",
    },
}


def classify_symptoms(text: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": SYMPTOM_CATEGORIES}}
    response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
    return response.json()


def show():
    st.title("🔍 Symptom Checker")
    st.caption("Uses **facebook/bart-large-mnli** (Zero-Shot Classification) from HuggingFace — Free!")

    if not os.environ.get("HF_TOKEN"):
        st.warning("🔑 Please enter your **HuggingFace Token** in the sidebar. Get it free at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)")

    st.markdown("### Describe Your Symptoms")

    # Common symptom chips
    st.markdown("**🏷️ Common symptoms (click to add):**")
    common = ["headache", "fever", "cough", "fatigue", "nausea", "chest pain",
              "shortness of breath", "dizziness", "rash", "muscle ache"]
    selected_chips = []
    chip_cols = st.columns(5)
    for i, symptom in enumerate(common):
        if chip_cols[i % 5].checkbox(symptom, key=f"chip_{i}"):
            selected_chips.append(symptom)

    additional = st.text_area(
        "Additional details:",
        placeholder="e.g., I've had a persistent headache for 2 days with sensitivity to light...",
        height=100,
    )

    full_input = ", ".join(selected_chips)
    if additional.strip():
        full_input = f"{full_input}, {additional}" if full_input else additional

    col1, col2 = st.columns([1, 4])
    analyze_btn = col1.button("🔍 Analyze", type="primary", use_container_width=True)

    if analyze_btn:
        if not full_input.strip():
            st.error("Please select symptoms or describe them above.")
            return

        hf_token = os.environ.get("HF_TOKEN", "")
        if not hf_token:
            st.error("HuggingFace token required for analysis.")
            return

        with st.spinner("🤖 Analyzing your symptoms using AI..."):
            try:
                result = classify_symptoms(full_input, hf_token)

                if "error" in result:
                    st.error(f"API Error: {result['error']}\n\nThe model may be loading. Try again in 20 seconds.")
                    return

                labels = result.get("labels", [])
                scores = result.get("scores", [])

                st.markdown("---")
                st.markdown("### 📊 Analysis Results")

                # Top 3 results
                top_n = 3
                for i in range(min(top_n, len(labels))):
                    cat = labels[i]
                    score = scores[i]
                    info = CATEGORY_INFO.get(cat, {})
                    icon = info.get("icon", "🔵")

                    with st.expander(f"{icon} **{cat.title()}** — Confidence: {score:.0%}", expanded=(i == 0)):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.progress(score)
                            st.markdown(f"**💡 Self-care advice:** {info.get('advice', 'Consult a healthcare provider.')}")
                            st.markdown(f"**🚨 See a doctor if:** {info.get('when_to_see_doctor', 'Symptoms persist or worsen.')}")

                st.error("⚠️ **Important:** This is an AI analysis for educational purposes only and is NOT a medical diagnosis. Please consult a qualified healthcare professional for any health concerns.")

            except requests.exceptions.Timeout:
                st.error("Request timed out. The HuggingFace model may be loading. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
