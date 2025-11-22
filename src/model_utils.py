import pickle
import numpy as np
import pandas as pd

def load_model():
    with open("src/model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

def classify_rain(df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify rain for 7-day forecast df
    Returns DataFrame with columns: date, rain_label, rain_proba
    """
    features = [
        "temperature_2m",
        "relative_humidity_2m",
        "dew_point_2m",
        "cloud_cover_low",
        "precipitation_probability"
        # "wind_speed_10m", # ถ้าจำเป็นเพิ่มได้
    ]

    X = df[features].values

    # Predict class
    y_pred = model.predict(X)

    # Predict probability
    y_proba = model.predict_proba(X)  # shape [n_samples, n_classes]

    # Map predicted class to label
    label_map = {0: "Not Rain", 1: "Rain"}
    y_label = [label_map[c] for c in y_pred]

    # Probability of predicted class
    proba_pred = [y_proba[i, c] for i, c in enumerate(y_pred)]

    # Return new DataFrame
    result_df = pd.DataFrame({
        "date": df["date"],
        "rain_label": y_label,
        "rain_proba": proba_pred
    })

    return result_df
