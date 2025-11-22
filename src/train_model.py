import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import pickle

# 1) โหลด dataset เดิมของคุณ
df = pd.read_csv("dataset.csv")

# 2) เตรียมฟีเจอร์และ target
X = df[[
    "relative_humidity_2m (%)",
    "cloud_cover_low (%)",
    "dew_point_2m (°C)",
    "temperature_2m (°C)",
    "wind_speed_100m (km/h)"
]]
y = df["target"]

# 3) แบ่ง train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4) เทรนโมเดล XGBoost Classifier
model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.9,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
)

model.fit(X_train, y_train)

print("Training complete with XGBoost!")

# 5) SAVE โมเดลเข้า src/model.pkl
with open("src/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("model saved successfully -> src/model.pkl")
