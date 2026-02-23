import streamlit as st
import os

SYSTEM_PROMPT = """You are HealthAI, a knowledgeable and empathetic health assistant.
- Provide clear, evidence-based health information
- Always remind users to consult a healthcare professional for diagnosis/treatment
- Be supportive, never alarmist
- Keep answers concise and easy to understand
- If asked about emergencies, immediately advise calling emergency services
"""

def get_groq_response(messages: list) -> str:
    """Call Groq API with the conversation history."""
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # free model on Groq
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except ImportError:
        return "⚠️ Please install the `groq` package: `pip install groq`"
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nMake sure your Groq API key is entered in the sidebar."


def show():
    st.title("💬 AI Health Chat")
    st.caption("Powered by **Groq + Llama 3.3 70B** — completely free!")

    # Warn if no key
    if not os.environ.get("GROQ_API_KEY"):
        st.warning("🔑 Please enter your **Groq API Key** in the sidebar to use the chat. Get it free at [console.groq.com](https://console.groq.com)")

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Suggested questions
    st.markdown("**💡 Try asking:**")
    suggestions = [
        "What are common symptoms of dehydration?",
        "How many hours of sleep do adults need?",
        "Tips to reduce stress naturally",
        "What foods boost the immune system?",
    ]
    cols = st.columns(2)
    for i, s in enumerate(suggestions):
        if cols[i % 2].button(s, key=f"sugg_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": s})
            with st.spinner("Thinking..."):
                reply = get_groq_response(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("---")

    # Render chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🏥"):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Ask a health question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🏥"):
            with st.spinner("HealthAI is thinking..."):
                reply = get_groq_response(st.session_state.chat_history)
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Clear button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
