# 🏥 HealthAI Assistant

A student project — AI-powered health companion built with **Streamlit**, **Groq (Free LLM)**, and **HuggingFace Free Models**.

## ✨ Features

| Feature | AI Model Used | Cost |
|---|---|---|
| 💬 AI Health Chat | Groq + Llama 3.3 70B | Free |
| 🔍 Symptom Checker | HuggingFace `facebook/bart-large-mnli` | Free |
| ⚖️ BMI & Health Metrics | Pure Python calculation | Free |
| 😊 Mood Tracker + Emotion Analysis | HuggingFace `j-hartmann/emotion-english-distilroberta-base` | Free |
| 🥗 Nutrition Guide + Meal Planner | Groq + Llama 3.3 70B | Free |

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/health-ai-assistant.git
cd health-ai-assistant
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get free API keys
- **Groq API Key** (Free, no credit card): [console.groq.com](https://console.groq.com)
- **HuggingFace Token** (Free): [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 4. Run the app
```bash
streamlit run app.py
```

> Enter your API keys in the sidebar when the app opens.

## 📁 Project Structure

```
health-ai-assistant/
├── app.py                  # Main Streamlit app + navigation
├── requirements.txt
├── README.md
└── pages/
    ├── __init__.py
    ├── home.py             # Landing page
    ├── chat.py             # AI Health Chat (Groq)
    ├── symptom_checker.py  # Symptom Analysis (HuggingFace)
    ├── bmi.py              # BMI, TDEE, Water Calculator
    ├── mood.py             # Mood Tracker + Emotion AI
    └── nutrition.py        # Nutrition Guide + Meal Planner
```

## 🔑 Environment Variables (Optional)

Instead of entering keys in the sidebar each time, create a `.env` file:

```env
GROQ_API_KEY=gsk_your_key_here
HF_TOKEN=hf_your_token_here
```

Then add this to the top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

And add `python-dotenv` to `requirements.txt`.

## ⚠️ Disclaimer

This application is built for **educational purposes only**. It does **not** replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (Llama 3.3 70B) — Free tier
- **NLP Models**: HuggingFace Inference API — Free tier
  - `facebook/bart-large-mnli` — Zero-shot classification
  - `j-hartmann/emotion-english-distilroberta-base` — Emotion detection
- **Language**: Python 3.9+

## 📸 Screenshots

> Add screenshots of your running app here!

---

Built with ❤️ as a student project | Powered by free AI APIs
