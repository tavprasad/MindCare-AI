import streamlit as st
import requests
import time

# CONFIG

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"
# API_URL = "http://34.226.152.222:8000/predict"

# CUSTOM CSS

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #334155
    );
}

.main-title{
    text-align:center;
    color:white;
    font-size:55px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:24px;
    margin-bottom:30px;
}

.metric-card{
    background-color:rgba(255,255,255,0.08);
    padding:15px;
    border-radius:15px;
    text-align:center;
}

.stButton > button{
    width:100%;
    height:60px;
    font-size:22px;
    font-weight:bold;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR

with st.sidebar:

    st.title("🧠 MindCare AI")

    st.markdown("---")

    st.info("""
### Features

✅ Real-Time Prediction

✅ Machine Learning Powered

✅ Lifestyle Analysis

✅ Mental Health Assessment

✅ FastAPI + Streamlit
""")

    st.markdown("---")

    st.success("💙 Built for Student Well-being")

# HEADER

st.markdown(
    """
<div class="main-title">
🧠 MindCare AI
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
🎓 Student Depression Risk Prediction System
</div>
""",
    unsafe_allow_html=True
)

st.progress(100)

st.caption("📋 Fill all details below for accurate prediction")

st.markdown("---")

# INPUTS

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "👤 Gender",
        ["Male", "Female"]
    )

    age = st.number_input(
        "🎂 Age",
        min_value=18,
        max_value=34,
        value=20
    )

    academic_pressure = st.slider(
        "📚 Academic Pressure",
        1,
        5,
        3
    )

    study_satisfaction = st.slider(
        "😊 Study Satisfaction",
        1,
        5,
        3
    )

    suicidal_thoughts = st.selectbox(
        "💭 Have you ever had suicidal thoughts?",
        ["Yes", "No"]
    )

with col2:

    sleep_duration = st.selectbox(
        "😴 Sleep Duration",
        [
            "Less than 5 hours",
            "5-6 hours",
            "7-8 hours",
            "More than 8 hours"
        ]
    )

    dietary_habits = st.selectbox(
        "🥗 Dietary Habits",
        [
            "Healthy",
            "Moderate",
            "Unhealthy"
        ]
    )

    study_hours = st.slider(
        "⏰ Study Hours",
        0,
        12,
        4
    )

    financial_stress = st.slider(
        "💰 Financial Stress",
        1,
        5,
        3
    )

    family_history = st.selectbox(
        "🧬 Family History of Mental Illness",
        ["Yes", "No"]
    )

# METRICS

st.markdown("---")

m1, m2, m3 = st.columns(3)

m1.metric(
    "📚 Academic Pressure",
    academic_pressure
)

m2.metric(
    "💰 Financial Stress",
    financial_stress
)

m3.metric(
    "⏰ Study Hours",
    study_hours
)

st.markdown("---")

# PREDICT BUTTON

if st.button("🚀 Predict Depression Risk"):

    payload = {
        "Gender": gender,
        "Age": age,
        "Academic_Pressure": academic_pressure,
        "Study_Satisfaction": study_satisfaction,
        "Sleep_Duration": sleep_duration,
        "Dietary_Habits": dietary_habits,
        "Suicidial_thoughts": suicidal_thoughts,
        "Study_hours": study_hours,
        "Financial_Stress": financial_stress,
        "Family_history": family_history
    }

    try:

        with st.spinner("🤖 AI Model is analyzing your profile..."):
            time.sleep(1)

            response = requests.post(
                API_URL,
                json=payload
            )

        if response.status_code == 200:

            prediction = response.json()["Predicted_category"]

            st.markdown("---")

            if prediction == 1:

                st.metric(
                label="Prediction Result",
                value="Yes" if prediction==1 else "No"
            )
                st.warning("⚠️ Elevated Depression Risk Identified")
                
                st.markdown("""
## 🚨 Recommendations

✅ Talk with trusted friends or family

✅ Maintain proper sleep schedule


✅ Practice physical exercise

✅ Seek professional counseling if needed

✅ Focus on work-life balance
""")

            else:

                st.success(
                    "🎉 Low Depression Risk Detected"
                )

                st.balloons()

   


        else:

            st.error(
                f"API Error: {response.text}"
            )

    except Exception as e:

        st.error(
            f"Connection Error: {e}"
        )

