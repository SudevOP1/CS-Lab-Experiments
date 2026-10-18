import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
THRESHOLD = 30

PROTOCOLS = {"zigbee": "Zigbee", "wifi": "WiFi", "bluetooth": "Bluetooth"}

# simulated devices, each technology sends data in its own raw format
DEVICES = [
    ("ioe/zigbee/sensor", "TEMP:28"),
    ("ioe/wifi/sensor", json.dumps({"device": "ESP32", "protocol": "WiFi", "temperature": 32})),
    ("ioe/bluetooth/sensor", "T:27"),
]

received = []

def normalize(topic, payload):
    protocol = PROTOCOLS[topic.split("/")[1]]
    try:
        temperature = float(json.loads(payload)["temperature"])
    except (ValueError, KeyError, TypeError):
        temperature = float(payload.replace("=", ":").split(":")[1])
    return {"protocol": protocol, "topic": topic, "temperature": temperature}

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"connected to broker {BROKER}:{PORT} ({reason_code})")
    client.subscribe("ioe/+/sensor")
    client.subscribe("ioe/alert")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    if msg.topic == "ioe/alert":
        print(f"  [ioe/alert] {payload}")
        return

    data = normalize(msg.topic, payload)
    received.append(data)
    print(f"\n[{msg.topic}] raw: {payload}")
    print(f"  normalized: {json.dumps({'protocol': data['protocol'], 'temperature': data['temperature']})}")

    alert = {
        "status": "WARNING" if data["temperature"] > THRESHOLD else "NORMAL",
        "source": data["protocol"],
        "temperature": data["temperature"],
    }
    client.publish("ioe/alert", json.dumps(alert))

if __name__ == "__main__":

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ioe-middleware")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_start()
    time.sleep(1)

    for topic, payload in DEVICES:
        client.publish(topic, payload)
        time.sleep(0.5)

    time.sleep(2)
    client.loop_stop()
    client.disconnect()

    print(f"\n----- interoperability evaluation -----")
    print(f"{'Source':<10}{'Technology':<12}{'MQTT Topic':<24}{'Temperature'}")
    for i, data in enumerate(received, 1):
        print(f"{'Sensor ' + str(i):<10}{data['protocol']:<12}{data['topic']:<24}{data['temperature']} C")
    print(f"\nmessages received: {len(received)}/{len(DEVICES)}\n")
