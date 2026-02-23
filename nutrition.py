import streamlit as st
import os

NUTRITION_SYSTEM_PROMPT = """You are NutriAI, a knowledgeable nutrition assistant.
- Provide science-backed dietary advice
- Create practical, realistic meal plans
- Consider user's dietary restrictions and goals
- Keep advice actionable and easy to follow
- Always remind that a registered dietitian can provide personalized guidance
- Use emojis to make responses engaging
- Format meal plans clearly with bullet points
"""

def get_nutrition_advice(prompt: str) -> str:
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": NUTRITION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.6,
        )
        return response.choices[0].message.content
    except ImportError:
        return "⚠️ Please install groq: `pip install groq`"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Nutrient data for common foods (per 100g)
FOOD_NUTRIENTS = {
    "Banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6},
    "Chicken Breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0},
    "Brown Rice": {"calories": 216, "protein": 5, "carbs": 45, "fat": 1.8, "fiber": 3.5},
    "Broccoli": {"calories": 55, "protein": 3.7, "carbs": 11, "fat": 0.6, "fiber": 5.1},
    "Egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "fiber": 0},
    "Salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13, "fiber": 0},
    "Oats": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7, "fiber": 11},
    "Greek Yogurt": {"calories": 100, "protein": 10, "carbs": 3.6, "fat": 5, "fiber": 0},
    "Almonds": {"calories": 579, "protein": 21, "carbs": 22, "fat": 50, "fiber": 12.5},
    "Sweet Potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "fiber": 3},
}


def show():
    st.title("🥗 Nutrition Guide")
    st.caption("AI-powered nutrition advice with **Groq Llama 3** + food nutrient lookup")

    if not os.environ.get("GROQ_API_KEY"):
        st.warning("🔑 Enter your **Groq API Key** in the sidebar for AI meal plans. Get it free at [console.groq.com](https://console.groq.com)")

    tab1, tab2, tab3 = st.tabs(["🤖 AI Meal Planner", "🔎 Food Lookup", "📋 Quick Tips"])

    # ── TAB 1: AI Meal Planner ─────────────────────────────────────────────────
    with tab1:
        st.markdown("### Personalized Meal Plan Generator")

        c1, c2 = st.columns(2)
        with c1:
            goal = st.selectbox("Your Goal", [
                "Weight Loss", "Muscle Gain", "Maintain Weight",
                "Improve Energy", "Heart Health", "Manage Diabetes"
            ])
            calories = st.number_input("Daily Calorie Target (kcal)", 1000, 4000, 2000, 100)
        with c2:
            diet_type = st.selectbox("Diet Preference", [
                "No preference", "Vegetarian", "Vegan", "Keto",
                "Mediterranean", "Gluten-Free", "Dairy-Free"
            ])
            allergies = st.multiselect("Allergies/Avoid:", [
                "Nuts", "Dairy", "Gluten", "Eggs", "Seafood", "Soy"
            ])

        extra_notes = st.text_input("Any special notes (optional):", placeholder="e.g., I eat dinner late, I dislike coriander")

        if st.button("🍽️ Generate Meal Plan", type="primary"):
            allergy_str = f"Avoid: {', '.join(allergies)}." if allergies else ""
            notes_str = f"Additional notes: {extra_notes}" if extra_notes else ""
            prompt = (
                f"Create a detailed 1-day meal plan for someone with the goal: {goal}. "
                f"Daily calorie target: {calories} kcal. Diet type: {diet_type}. "
                f"{allergy_str} {notes_str} "
                f"Include breakfast, lunch, dinner, and 2 snacks. "
                f"For each meal, list foods and approximate portions. "
                f"End with 3 practical tips for achieving the goal."
            )
            with st.spinner("🤖 Creating your personalized meal plan..."):
                plan = get_nutrition_advice(prompt)
            st.markdown("---")
            st.markdown("### 📋 Your Personalized Meal Plan")
            st.markdown(plan)

    # ── TAB 2: Food Lookup ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("### Food Nutrient Lookup")
        foods_selected = st.multiselect("Select foods to compare:", list(FOOD_NUTRIENTS.keys()))

        if foods_selected:
            import pandas as pd
            rows = []
            for food in foods_selected:
                n = FOOD_NUTRIENTS[food]
                rows.append({"Food": food, **n})
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Bar chart for calories
            st.markdown("**📊 Calorie Comparison:**")
            cal_df = df[["Food", "calories"]].set_index("Food")
            st.bar_chart(cal_df)
        else:
            st.info("Select one or more foods from the dropdown above to see their nutritional data.")

    # ── TAB 3: Quick Tips ──────────────────────────────────────────────────────
    with tab3:
        st.markdown("### 🌟 Evidence-Based Nutrition Tips")

        tips = {
            "🥦 Eat the Rainbow": "Aim for 5–9 servings of colorful fruits and vegetables daily for diverse phytonutrients.",
            "💧 Hydrate Before Hunger": "Often mistaken for hunger, dehydration can trigger unnecessary snacking. Drink water first.",
            "🥚 Protein at Every Meal": "Including protein (eggs, legumes, meat, tofu) increases satiety and preserves muscle mass.",
            "🌾 Choose Whole Grains": "Swap refined grains for whole grains to improve fiber intake and blood sugar control.",
            "🥑 Healthy Fats Are Essential": "Avocado, nuts, olive oil, and fatty fish support brain health and hormone production.",
            "⏰ Mindful Eating": "Eat slowly, without screens. It takes 20 minutes for your brain to register fullness.",
            "🍽️ Portion Awareness": "Use the plate method: ½ vegetables, ¼ lean protein, ¼ whole grains.",
            "🚫 Limit Ultra-Processed Foods": "Foods with long ingredient lists and added sugars are linked to multiple chronic diseases.",
        }

        cols = st.columns(2)
        for i, (title, tip) in enumerate(tips.items()):
            cols[i % 2].markdown(f"""
            <div class="feature-card">
            <b>{title}</b><br><small>{tip}</small>
            </div>
            """, unsafe_allow_html=True)
