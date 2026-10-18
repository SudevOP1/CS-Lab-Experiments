import os
import json
import time
import random
import paho.mqtt.client as mqtt

# local broker the soil node publishes to (edge side)
EDGE_BROKER = os.getenv("MQTT_BROKER", "localhost")
EDGE_PORT = 1883
RAW_TOPIC = "ioe/exp4/soil/raw"

# aws iot core (cloud side). if AWS_ENDPOINT is not set, the local broker stands in for the cloud
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")  # e.g. xxxxxxxx-ats.iot.ap-south-1.amazonaws.com
AWS_CA = os.getenv("AWS_CA", "certs/AmazonRootCA1.pem")
AWS_CERT = os.getenv("AWS_CERT", "certs/certificate.pem.crt")
AWS_KEY = os.getenv("AWS_KEY", "certs/private.pem.key")
CLOUD_TOPIC = "ioe/exp4/soil/processed"

THRESHOLD = 30  # below this soil is dry -> alert
DEADBAND = 2    # change smaller than this is treated as redundant

last = {"moisture": None, "alert": None}
stats = {"received": 0, "invalid": 0, "redundant": 0, "forwarded": 0, "alerts": 0}

def simulate_reading(i):
    # stands in for the esp8266 soil node when hardware is unavailable
    moisture = max(0, round(55 - i * 2.5 + random.uniform(-1, 1)))
    if i % 4 == 1:
        moisture = last["moisture"] if last["moisture"] is not None else moisture
    if i == 7:
        moisture = 140
    return json.dumps({"device": "soil-node-01", "moisture": moisture})

def edge_filter(data):
    moisture = data.get("moisture")
    if not isinstance(moisture, (int, float)) or not 0 <= moisture <= 100:
        return None, "invalid"

    alert = moisture < THRESHOLD
    if last["moisture"] is not None and abs(moisture - last["moisture"]) < DEADBAND and alert == last["alert"]:
        return None, "redundant"

    last["moisture"] = moisture
    last["alert"] = alert
    return {
        "device": data["device"],
        "moisture": moisture,
        "status": "DRY - IRRIGATE" if alert else "OK",
        "alert": alert,
        "timestamp": int(time.time()),
    }, None

def connect_cloud():
    cloud = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="exp4-edge-gateway")
    if AWS_ENDPOINT:
        cloud.tls_set(ca_certs=AWS_CA, certfile=AWS_CERT, keyfile=AWS_KEY)
        cloud.connect(AWS_ENDPOINT, 8883)
        print(f"cloud: aws iot core {AWS_ENDPOINT}")
    else:
        cloud.connect(EDGE_BROKER, EDGE_PORT)
        print(f"cloud: AWS_ENDPOINT not set, using local broker as cloud")
    cloud.loop_start()
    return cloud

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"edge: connected to {EDGE_BROKER}:{EDGE_PORT} ({reason_code})")
    client.subscribe(RAW_TOPIC)

def on_message(client, userdata, msg):
    stats["received"] += 1
    try:
        data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        data = {}

    result, reason = edge_filter(data)
    if reason:
        stats[reason] += 1
        print(f"  {str(data.get('moisture')):>8}   DROPPED ({reason})")
        return

    # aws iot rule stores this in dynamodb, e.g. SELECT * FROM 'ioe/exp4/soil/processed'
    cloud.publish(CLOUD_TOPIC, json.dumps(result), qos=1)
    stats["forwarded"] += 1
    if result["alert"]:
        stats["alerts"] += 1
    print(f"  {result['moisture']:>8}   FORWARDED -> {result['status']}")

if __name__ == "__main__":

    random.seed(4)
    cloud = connect_cloud()

    edge = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="exp4-edge")
    edge.on_connect = on_connect
    edge.on_message = on_message
    edge.connect(EDGE_BROKER, EDGE_PORT)
    edge.loop_start()
    time.sleep(1)

    print(f"\n----- edge processing (threshold {THRESHOLD}%, deadband {DEADBAND}%) -----")
    print(f"  {'moisture':>8}   action")

    for i in range(16):
        edge.publish(RAW_TOPIC, simulate_reading(i))
        time.sleep(1)

    time.sleep(1)
    edge.loop_stop()
    edge.disconnect()
    cloud.loop_stop()
    cloud.disconnect()

    print(f"\n----- summary -----")
    print(f"readings received: {stats['received']}")
    print(f"invalid dropped: {stats['invalid']}")
    print(f"redundant dropped: {stats['redundant']}")
    print(f"forwarded to cloud: {stats['forwarded']}")
    print(f"dry alerts: {stats['alerts']}")
    print(f"bandwidth saved: {(1 - stats['forwarded'] / stats['received']) * 100:.1f}%\n")
