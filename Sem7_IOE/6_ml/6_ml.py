import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

CSV_FILE = "soil_moisture_data.csv"
LABELS = {0: "Dry", 1: "Normal", 2: "Wet"}
ACTIONS = {"Dry": "Turn irrigation ON", "Normal": "Keep irrigation OFF", "Wet": "Keep irrigation OFF"}

def label(moisture):
    if moisture < 30:
        return "Dry"
    if moisture < 65:
        return "Normal"
    return "Wet"

def generate_data(n=300):
    # simulated soil moisture readings, used only if real soil_moisture_data.csv is not present
    np.random.seed(42)
    timestamps = pd.date_range("10:00:00", periods=n, freq="5s").strftime("%H:%M:%S")
    moisture = np.random.randint(5, 96, n)
    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Soil Moisture": moisture,
        "Condition": [label(m) for m in moisture],
    })
    df.to_csv(CSV_FILE, index=False)

if __name__ == "__main__":

    if not os.path.exists(CSV_FILE):
        generate_data()

    # step 4: import
    data = pd.read_csv(CSV_FILE)
    print(f"\n----- first 5 rows -----")
    print(data.head())

    # step 5: check and prepare
    print(f"\n----- missing values -----")
    print(data.isnull().sum())
    data = data.dropna()
    data = data[(data["Soil Moisture"] >= 0) & (data["Soil Moisture"] <= 100)]
    print(f"\nduplicate rows: {data.duplicated().sum()}")
    print(f"rows after cleaning: {len(data)}")

    # step 6: features and target (0 -> dry, 1 -> normal, 2 -> wet)
    X = data[["Soil Moisture"]]
    y = data["Condition"].map({v: k for k, v in LABELS.items()})

    # step 7: split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # step 8: train
    model = DecisionTreeClassifier(max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    # step 9: evaluate
    y_pred = model.predict(X_test)
    print(f"\n----- evaluation -----")
    print(f"accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print(f"\nconfusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"\nclassification report:")
    print(classification_report(y_test, y_pred, target_names=list(LABELS.values())))

    # step 10 - 12: real-time prediction and irrigation decision
    # these readings would arrive from the esp8266 over serial/mqtt
    print(f"----- real-time prediction -----")
    incoming = [12, 27, 35, 50, 64, 70, 88, 20]
    counts = {"Dry": 0, "Normal": 0, "Wet": 0}

    for reading in incoming:
        sample = pd.DataFrame({"Soil Moisture": [reading]})
        condition = LABELS[model.predict(sample)[0]]
        counts[condition] += 1
        print(f"moisture: {reading:3d}% -> {condition:6s} -> {ACTIONS[condition]}")

    print(f"\nevent counts: {counts}\n")
