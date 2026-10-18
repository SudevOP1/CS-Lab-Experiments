import os
import json
import time
import random
import paho.mqtt.client as mqtt

# credentials come from environment variables, not source code
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
USERNAME = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASS")

SENSOR_TOPIC = "ioe/exp9/campus/sensor"
STATUS_TOPIC = "ioe/exp9/campus/status"
ALERT_TOPIC = "ioe/exp9/campus/alert"

MAX_OCCUPANCY = 40
HIGH_TEMP = 35
LOW_LIGHT = 150
WINDOW = 5

LIMITS = {
    "temperature_c": (-10, 60),
    "occupancy": (0, 500),
    "light_lux": (0, 100000),
}

temps = []
stats = {"valid": 0, "invalid": 0, "alerts": 0, "peak_occupancy": 0}

def simulate_reading(i):
    # stands in for the esp32 campus node when hardware is unavailable
    reading = {
        "device": "campus-node-01",
        "application": "SmartCampus",
        "temperature_c": round(28 + i * 0.6 + random.uniform(-0.5, 0.5), 1),
        "occupancy": random.randint(5, 50),
        "light_lux": random.randint(80, 500),
    }
    if i == 4:
        del reading["occupancy"]
    if i == 8:
        reading["temperature_c"] = "error"
    if i == 11:
        reading["light_lux"] = -50
    return json.dumps(reading)

def validate(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None, "payload is not valid json"
    for field, (low, high) in LIMITS.items():
        if field not in data:
            return None, f"missing field '{field}'"
        value = data[field]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return None, f"'{field}' is not numeric ({value!r})"
        if not low <= value <= high:
            return None, f"'{field}' out of range ({value})"
    return data, None

def analyze(data):
    temps.append(data["temperature_c"])
    if len(temps) > WINDOW:
        temps.pop(0)

    if data["temperature_c"] >= HIGH_TEMP:
        status = "HIGH TEMPERATURE"
    elif data["occupancy"] > MAX_OCCUPANCY:
        status = "HIGH OCCUPANCY"
    elif data["light_lux"] < LOW_LIGHT and data["occupancy"] > 0:
        status = "LOW LIGHT"
    else:
        status = "NORMAL"

    return {
        "application": "SmartCampus",
        "device": data["device"],
        "status": status,
        "temperature_c": data["temperature_c"],
        "avg_temperature_c": round(sum(temps) / len(temps), 2),
        "occupancy": data["occupancy"],
        "occupancy_pct": round(data["occupancy"] / MAX_OCCUPANCY * 100, 1),
        "light_lux": data["light_lux"],
    }

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"connected to broker {BROKER}:{PORT} ({reason_code})")
    client.subscribe(SENSOR_TOPIC)

def on_message(client, userdata, msg):
    data, error = validate(msg.payload.decode())
    if error:
        stats["invalid"] += 1
        print(f"  REJECTED  {error}")
        return

    result = analyze(data)
    stats["valid"] += 1
    stats["peak_occupancy"] = max(stats["peak_occupancy"], result["occupancy"])
    client.publish(STATUS_TOPIC, json.dumps(result))

    print(f"  {result['temperature_c']:>6.1f} {result['avg_temperature_c']:>8.2f} "
          f"{result['occupancy']:>5d} ({result['occupancy_pct']:>5.1f}%) "
          f"{result['light_lux']:>6d}   {result['status']}")

    if result["status"] != "NORMAL":
        alert = {"status": "WARNING", "reason": result["status"], "device": result["device"]}
        client.publish(ALERT_TOPIC, json.dumps(alert))
        stats["alerts"] += 1

if __name__ == "__main__":

    random.seed(7)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="campus-app")
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_start()
    time.sleep(1)

    print(f"\n----- smart campus dashboard (room 101) -----")
    print(f"  {'temp':>6} {'avg_temp':>8} {'occupancy':>13} {'light':>6}   status")

    for i in range(14):
        client.publish(SENSOR_TOPIC, simulate_reading(i))
        time.sleep(1)

    time.sleep(1)
    client.loop_stop()
    client.disconnect()

    print(f"\n----- summary -----")
    print(f"valid readings: {stats['valid']}")
    print(f"rejected readings: {stats['invalid']}")
    print(f"alerts raised: {stats['alerts']}")
    print(f"peak occupancy: {stats['peak_occupancy']}")
    print(f"avg temperature (last {WINDOW}): {sum(temps) / max(len(temps), 1):.2f} C\n")
