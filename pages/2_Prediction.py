import streamlit as st
from src.utils import fetch_open_meteo, fetch_open_meteo_hourly
from src.model_utils import classify_rain_daily, classify_rain_hourly

# Wide layout
st.set_page_config(layout="wide")

st.title("🌦️ 7-Day Rain Prediction")

# -----------------------
# FETCH DATA
# -----------------------
daily_df = fetch_open_meteo()          # daily summary
hourly_df = fetch_open_meteo_hourly()  # hourly data (7*24 rows)

# -----------------------
# CLASSIFY DAILY
# -----------------------
daily_result = classify_rain_daily(daily_df)

# -----------------------
# FORECAST OVERVIEW (7 DAYS)
# -----------------------
st.subheader("📅 Forecast Overview (7 Days)")

for idx, row in daily_result.iterrows():
    date = row["date"]
    label = row["rain_label"]
    proba = row["rain_proba"]
    icon = "🌧️" if label == "Rain" else "☀️"

    # DAILY overview row
    st.markdown(f"""
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
    """, unsafe_allow_html=True)

    # -----------------------
    # EXPANDER: hourly forecast for this day
    # -----------------------
    with st.expander(f"🕒 Hourly Forecast for {date}"):

        day_hourly = hourly_df[hourly_df["date"] == str(date)]
        hourly_result = classify_rain_hourly(day_hourly)

        # --- FLEX BAR PER HOUR ---
        for i, hr in hourly_result.iterrows():
            hour = hr["hour"]
            label_hr = hr["rain_label"]
            proba_hr = hr["rain_proba"]
            icon_hr = "🌧️" if label_hr == "Rain" else "☀️"

            st.markdown(f"""
            <div style='display:flex; align-items:center; margin-bottom:6px;'>
                <div style='flex:1; text-align:center; color:white;'>{hour}:00</div>
                <div style='flex:1; text-align:center; font-size:20px'>{icon_hr}</div>
                <div style='flex:6; display:flex; align-items:center;'>
                    <div style='flex-grow:1; height:16px; border-radius:8px; background-color:#333; margin-right:8px; position:relative;'>
                        <div style='width:{proba_hr*100}%; height:100%; border-radius:8px; background: linear-gradient(90deg, #FBCA0A, #F05A28);'></div>
                    </div>
                    <div style='min-width:35px; text-align:center; color:white; font-weight:bold;'>{proba_hr*100:.0f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # --- TABLE PER HOUR BELOW ---
        table_df = hourly_result.copy()
        table_df["Probability"] = table_df["rain_proba"].apply(lambda x: f"{x*100:.0f}%")
        st.markdown("**Hourly Data Table:**")
        st.dataframe(table_df[["hour", "rain_label", "Probability"]], use_container_width=True)
