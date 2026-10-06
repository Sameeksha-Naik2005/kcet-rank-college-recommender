import streamlit as st
import requests
import pandas as pd
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="KCET Rank Predictor & College Finder",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3, h4, h5 { color: #aee1f9; }
p, label, .stMarkdown { color: #f0f0f0; }
button, .stButton button {
    background: linear-gradient(90deg, #36d1dc, #5b86e5);
    color: white !important;
    border-radius: 8px;
    border: none;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
}
button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #5b86e5, #36d1dc);
}
</style>
""", unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.stage = 1
if "predicted_rank" not in st.session_state:
    st.session_state.predicted_rank = None
if "filters" not in st.session_state:
    st.session_state.filters = {}

@st.cache_data
def load_filters():
    r = requests.get(f"{BACKEND_URL}/filters")
    return r.json()

filters_data = load_filters()

if st.session_state.stage == 1:
    st.title("🎯 KCET Rank Predictor")
    st.markdown("Enter your marks to predict your KCET rank")

    with st.form("predict_form"):
        kcet_marks = st.number_input("KCET Marks (out of 180)", 0, 180, 100)
        board_marks = st.number_input("Board Marks (out of 300)", 0, 300, 200)
        year = st.selectbox("Exam Year", [2022, 2023, 2024, 2025, 2026])
        submit = st.form_submit_button("🔮 Predict Rank")

    if submit:
        payload = {
            "kcet_marks": kcet_marks,
            "board_marks": board_marks,
            "year_attended": year
        }

        res = requests.post(f"{BACKEND_URL}/predict", json=payload)

        if res.status_code == 200:
            rank = res.json()["estimated_rank"]
            st.session_state.predicted_rank = rank
            st.success(f"✅ Your Predicted Rank: **{rank}**")
            st.session_state.stage = 2
            st.rerun()
        else:
            st.error("Prediction failed. Backend error.")


elif st.session_state.stage == 2:
    st.title("🏫 College Finder - Set Your Preferences")
    st.info(f"Your Predicted Rank: **{st.session_state.predicted_rank}**")

    with st.form("filters_form"):
        branches = st.multiselect(
            "🎓 Preferred Branch(es):",
            filters_data["branch"],
            default=["Any Branch"]
        )
        location = st.selectbox("📍 Preferred Location:", filters_data["location"])
        college_type = st.selectbox("🏛 University Type:", filters_data["type"])
        search = st.form_submit_button("🔍 Search Colleges")

    if search:
        st.session_state.filters = {
            "branches": branches,
            "location": location,
            "college_type": college_type
        }
        st.session_state.stage = 3
        st.rerun()

elif st.session_state.stage == 3:
    st.title("📊 Eligible Colleges for You")
    st.info(f"Predicted Rank: **{st.session_state.predicted_rank}**")

    payload = {
        "rank": st.session_state.predicted_rank,
        **st.session_state.filters
    }

    res = requests.post(f"{BACKEND_URL}/recommandation/", json=payload)

    if res.status_code != 200:
        st.error("Failed to fetch colleges")
    else:
        data = res.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("❌ No colleges found with given criteria.")
        else:
            st.success(f"✅ Found {len(df)} colleges")

            if "Websites" in df.columns and "college name" in df.columns:
                df["college name"] = df.apply(
                    lambda r: f'<a href="{r["Websites"]}" target="_blank">{r["college name"]}</a>'
                    if isinstance(r.get("Websites"), str) and r["Websites"].startswith("http")
                    else r["college name"],
                    axis=1
                )

            show_cols = ["College Code", "college name", "Course Name", "Location", "Type of College", "GM"]
            show_cols = [c for c in show_cols if c in df.columns]

            st.markdown(df[show_cols].to_html(escape=False, index=False), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back to Criteria"):
            st.session_state.stage = 2
    with col2:
        if st.button("🔄 Reset Prediction"):
            st.session_state.stage = 1
            st.session_state.predicted_rank = None
            st.session_state.filters = {}
