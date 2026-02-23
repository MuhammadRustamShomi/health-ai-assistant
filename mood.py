import streamlit as st
import os
import requests
from datetime import datetime, date
import json

HF_SENTIMENT_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
HF_EMOTION_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"

MOOD_EMOJIS = {1: "😢", 2: "😟", 3: "😐", 4: "🙂", 5: "😄"}
MOOD_LABELS = {1: "Very Low", 2: "Low", 3: "Neutral", 4: "Good", 5: "Excellent"}


def analyze_text_emotion(text: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(HF_EMOTION_URL, headers=headers, json={"inputs": text}, timeout=30)
        return r.json()
    except Exception:
        return {}


def show():
    st.title("😊 Mood Tracker")
    st.caption("Track your mental wellness with **AI emotion analysis** — HuggingFace Free Models")

    # Init session state storage
    if "mood_entries" not in st.session_state:
        st.session_state.mood_entries = []

    tab1, tab2 = st.tabs(["📝 Log Mood", "📊 My History"])

    with tab1:
        st.markdown("### How are you feeling today?")

        mood_score = st.select_slider(
            "Mood Level",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: f"{MOOD_EMOJIS[x]} {MOOD_LABELS[x]}",
        )

        journal = st.text_area(
            "📓 Journal Entry (optional — AI will analyze emotions)",
            placeholder="Write how you're feeling... 'I felt anxious today because of...'",
            height=120,
        )

        factors = st.multiselect(
            "Contributing factors:",
            ["Sleep", "Exercise", "Diet", "Work stress", "Social connection",
             "Weather", "Health", "Personal achievement", "Relationships"],
        )

        col1, col2 = st.columns([1, 4])
        save_btn = col1.button("💾 Save Entry", type="primary", use_container_width=True)

        if save_btn:
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

            hf_token = os.environ.get("HF_TOKEN", "")
            if journal.strip() and hf_token:
                with st.spinner("🤖 Analyzing emotions in your journal..."):
                    result = analyze_text_emotion(journal, hf_token)
                    if isinstance(result, list) and len(result) > 0:
                        emotions = result[0] if isinstance(result[0], list) else result
                        entry["emotions"] = sorted(emotions, key=lambda x: x.get("score", 0), reverse=True)[:3]

            st.session_state.mood_entries.append(entry)
            st.success(f"✅ Entry saved for {entry['date']} at {entry['time']}")

            if entry["emotions"]:
                st.markdown("**🧠 Detected Emotions:**")
                for emo in entry["emotions"]:
                    label = emo.get("label", "").title()
                    score = emo.get("score", 0)
                    st.progress(score, text=f"{label}: {score:.0%}")

            # Wellbeing tips based on mood
            st.markdown("---")
            st.markdown("**💡 Personalized Tip:**")
            tips = {
                1: "🌱 Be gentle with yourself. Reach out to someone you trust. Consider calling a helpline if needed.",
                2: "🌿 Try a short walk outside. Even 10 minutes of fresh air can shift your mood.",
                3: "☀️ Routine helps — stick to meal times, hydrate well, and get enough sleep.",
                4: "✨ Great to hear! Use this energy for a creative or social activity you enjoy.",
                5: "🎉 Wonderful! Celebrate this feeling and journal what contributed to it.",
            }
            st.info(tips[mood_score])

            if mood_score <= 2:
                st.error("If you're struggling, please reach out: **Crisis Text Line** — Text HOME to 741741")

    with tab2:
        st.markdown("### Your Mood History")

        if not st.session_state.mood_entries:
            st.info("No entries yet. Log your first mood in the 'Log Mood' tab!")
            return

        entries = st.session_state.mood_entries

        # Summary stats
        avg_mood = sum(e["mood_score"] for e in entries) / len(entries)
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Entries", len(entries))
        s2.metric("Average Mood", f"{MOOD_EMOJIS[round(avg_mood)]} {avg_mood:.1f}/5")
        s3.metric("Latest Mood", f"{entries[-1]['emoji']} {entries[-1]['mood_label']}")

        # Mood chart
        st.markdown("---")
        st.markdown("**📈 Mood Trend:**")
        chart_data = {"date": [], "score": []}
        for e in entries:
            chart_data["date"].append(f"{e['date']} {e['time']}")
            chart_data["score"].append(e["mood_score"])

        import pandas as pd
        df = pd.DataFrame(chart_data)
        st.line_chart(df.set_index("date")["score"])

        # Entries list
        st.markdown("---")
        st.markdown("**📋 Recent Entries:**")
        for e in reversed(entries[-10:]):
            with st.expander(f"{e['emoji']} {e['date']} {e['time']} — {e['mood_label']}"):
                if e["journal"]:
                    st.markdown(f"📓 *{e['journal']}*")
                if e["factors"]:
                    st.markdown(f"**Factors:** {', '.join(e['factors'])}")
                if e["emotions"]:
                    st.markdown("**Detected emotions:**")
                    for emo in e["emotions"]:
                        st.caption(f"• {emo.get('label', '').title()}: {emo.get('score', 0):.0%}")

        if st.button("🗑️ Clear History"):
            st.session_state.mood_entries = []
            st.rerun()
