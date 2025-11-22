import streamlit as st
from src.utils import fetch_open_meteo
from src.model_utils import classify_rain

# Wide layout
st.set_page_config(layout="wide")

st.title("🌦️ 7-Day Rain Prediction")

# Fetch and classify
df = fetch_open_meteo()
result = classify_rain(df)

# -----------------------
# Forecast Overview (bigger, full-width like dashboard)
# -----------------------
st.subheader("📅 Forecast Overview")

for idx, row in result.iterrows():
    date = row["date"]
    label = row["rain_label"]
    proba = row["rain_proba"]
    icon = "🌧️" if label == "Rain" else "☀️"

    row_html = f"""
    <div style='display:flex; align-items:center; margin-bottom:12px;'>
        <div style='flex:1; text-align:center; color:white; font-size:16px'>{date}</div>
        <div style='flex:1; text-align:center; font-size:28px'>{icon}</div>
        <div style='flex:6; display:flex; align-items:center;'>
            <div style='flex-grow:1; height:20px; border-radius:10px; background-color:#333; margin-right:10px; position:relative;'>
                <div style='width:{proba*100}%; height:100%; border-radius:10px; background: linear-gradient(90deg, #FBCA0A, #F05A28);'></div>
            </div>
            <div style='min-width:45px; text-align:center; color:white; font-weight:bold; font-size:16px'>{proba*100:.0f}%</div>
        </div>
    </div>
    """
    st.markdown(row_html, unsafe_allow_html=True)
# Prepare display table
display_df = result.copy()
display_df["Probability"] = display_df["rain_proba"].apply(lambda x: f"{x*100:.0f}%")

st.subheader("🔍 Prediction Result (7 Days)")

# Minimal dark-style table
st.markdown("""
    <style>
    .stDataFrame div[data-testid="stVerticalBlock"] {
        background-color: rgba(30,30,30,0.7);
        color: #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

st.dataframe(display_df[["date", "rain_label", "Probability"]], use_container_width=True)