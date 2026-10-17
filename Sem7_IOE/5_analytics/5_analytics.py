import os
import numpy as np
import pandas as pd

CSV_FILE = "sensor_data.csv"
WINDOW = 10

def generate_data(n=300):
    # simulated dht11 readings, used only if real sensor_data.csv is not present
    np.random.seed(42)
    timestamps = pd.date_range("10:00:00", periods=n, freq="5s").strftime("%H:%M:%S")
    temperature = 28 + np.linspace(0, 3, n) + np.random.normal(0, 0.3, n)
    humidity = 62 - np.linspace(0, 5, n) + np.random.normal(0, 1, n)

    for i in [50, 140, 230]:
        temperature[i] += 8
    for i in [90, 200]:
        humidity[i] -= 20
    temperature[[30, 170]] = np.nan
    humidity[110] = np.nan

    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Temperature": temperature.round(1),
        "Humidity": humidity.round(1),
    })
    df.to_csv(CSV_FILE, index=False)

def zscore_anomalies(series, threshold=3):
    z = (series - series.mean()) / series.std()
    return z.abs() > threshold

def iqr_anomalies(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (series < lower) | (series > upper), lower, upper

def trend(series):
    slope = np.polyfit(np.arange(len(series)), series, 1)[0]
    if slope > 0.001:
        return slope, "Increasing"
    if slope < -0.001:
        return slope, "Decreasing"
    return slope, "Stable"

if __name__ == "__main__":

    if not os.path.exists(CSV_FILE):
        generate_data()

    # step 4: import
    data = pd.read_csv(CSV_FILE)
    print(f"\n----- first 5 rows -----")
    print(data.head())

    # step 5: missing values
    print(f"\n----- missing values -----")
    print(data.isnull().sum())
    data[["Temperature", "Humidity"]] = data[["Temperature", "Humidity"]].interpolate()

    # step 6: basic statistics
    print(f"\n----- basic statistics -----")
    print(data.describe().round(2))

    for col in ["Temperature", "Humidity"]:
        series = data[col]

        print(f"\n----- {col} -----")
        print(f"average: {series.mean():.2f}")

        data[f"{col}_MA"] = series.rolling(WINDOW).mean()
        print(f"last moving average ({WINDOW} readings): {data[f'{col}_MA'].iloc[-1]:.2f}")

        z_mask = zscore_anomalies(series)
        data[f"{col}_ZAnomaly"] = z_mask
        print(f"z-score anomalies: {z_mask.sum()}")
        print(data.loc[z_mask, ["Timestamp", col]].to_string(index=False))

        iqr_mask, lower, upper = iqr_anomalies(series)
        data[f"{col}_IQRAnomaly"] = iqr_mask
        print(f"iqr range: [{lower:.2f}, {upper:.2f}]")
        print(f"iqr anomalies: {iqr_mask.sum()}")
        print(data.loc[iqr_mask, ["Timestamp", col]].to_string(index=False))

        # step 7: trend analysis
        slope, direction = trend(series)
        print(f"trend slope: {slope:.4f} per reading -> {direction}")

        # step 8: percentage change
        data[f"{col}_PctChange"] = series.pct_change() * 100
        total_change = (series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100
        print(f"overall percentage change: {total_change:.2f}%")

    # step 9: export for power bi / grafana dashboard
    data.to_csv("sensor_data_processed.csv", index=False)
    print(f"\nprocessed data saved to sensor_data_processed.csv (import in power bi)\n")
