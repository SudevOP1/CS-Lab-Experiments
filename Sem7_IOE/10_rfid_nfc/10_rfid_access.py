import os
import csv
import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
USERNAME = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASS")

SCAN_TOPIC = "ioe/rfid/scan"
EVENT_TOPIC = "ioe/rfid/access-events"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_FILE = os.path.join(BASE_DIR, "10_tag_registry.json")
LOG_FILE = "access_log.csv"
LOG_FIELDS = ["timestamp", "reader_id", "location", "tag_uid", "entity_id", "event_type", "decision", "reason"]

# simulated tag scans, stands in for the esp32 + mfrc522 reader
SCANS = [
    {"reader_id": "LAB-A-READER-01", "tag_uid": "a1 b2 c3 d4", "event_type": "ACCESS_ATTEMPT"},
    {"reader_id": "LAB-A-READER-01", "tag_uid": "DE AD BE EF", "event_type": "ACCESS_ATTEMPT"},
    {"reader_id": "LAB-A-READER-01", "tag_uid": "55 66 77 88", "event_type": "ACCESS_ATTEMPT"},
    {"reader_id": "LAB-B-READER-01", "tag_uid": "A1 B2 C3 D4", "event_type": "ACCESS_ATTEMPT"},
    {"reader_id": "LAB-B-READER-01", "tag_uid": "99 AA BB CC", "event_type": "ACCESS_ATTEMPT"},
    {"reader_id": "STORE-READER-01", "tag_uid": "11 22 33 44", "event_type": "ASSET_SCAN"},
    {"reader_id": "LAB-A-READER-01", "tag_uid": "11 22 33 44", "event_type": "ASSET_SCAN"},
    {"reader_id": "LAB-A-READER-01", "event_type": "ACCESS_ATTEMPT"},
]

with open(REGISTRY_FILE) as f:
    registry = json.load(f)

events = []

def normalize_uid(uid):
    return uid.replace(" ", "").replace(":", "").upper()

def decide(uid, location, event_type):
    tag = registry["tags"].get(uid)
    if tag is None:
        return None, "ACCESS_DENIED", "tag not registered"
    if tag["status"] != "ACTIVE":
        return tag["entity_id"], "ACCESS_DENIED", "tag inactive"
    if event_type == "ASSET_SCAN":
        return tag["entity_id"], "ASSET_RECORDED", f"asset seen at {location}"
    if location not in tag["locations"]:
        return tag["entity_id"], "ACCESS_DENIED", f"no permission for {location}"
    return tag["entity_id"], "ACCESS_GRANTED", "authorized"

def process(scan):
    if not isinstance(scan.get("tag_uid"), str) or scan.get("reader_id") not in registry["readers"]:
        return None

    uid = normalize_uid(scan["tag_uid"])
    location = registry["readers"][scan["reader_id"]]
    event_type = scan.get("event_type", "ACCESS_ATTEMPT")
    entity_id, decision, reason = decide(uid, location, event_type)

    return {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "reader_id": scan["reader_id"],
        "location": location,
        "tag_uid": uid,
        "entity_id": entity_id or "UNKNOWN",
        "event_type": event_type,
        "decision": decision,
        "reason": reason,
    }

def log_event(event):
    new_file = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(event)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"connected to broker {BROKER}:{PORT} ({reason_code})")
    client.subscribe(SCAN_TOPIC)

def on_message(client, userdata, msg):
    try:
        scan = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        scan = {}

    event = process(scan)
    if event is None:
        print(f"\n[scan] {msg.payload.decode()}\n  REJECTED: invalid scan message")
        return

    events.append(event)
    log_event(event)
    client.publish(EVENT_TOPIC, json.dumps(event))
    print(f"\n[scan] {scan['reader_id']} uid='{scan['tag_uid']}' -> {event['tag_uid']}")
    print(f"  {event['entity_id']:<10} {event['decision']:<15} ({event['reason']})")

if __name__ == "__main__":

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="rfid-app")
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_start()
    time.sleep(1)

    for scan in SCANS:
        client.publish(SCAN_TOPIC, json.dumps(scan))
        time.sleep(1)

    time.sleep(1)
    client.loop_stop()
    client.disconnect()

    print(f"\n----- access log dashboard -----")
    print(f"{'Timestamp':<27}{'Reader':<18}{'Tag UID':<11}{'Entity':<11}{'Event Type':<16}{'Decision'}")
    for e in events:
        print(f"{e['timestamp']:<27}{e['reader_id']:<18}{e['tag_uid']:<11}{e['entity_id']:<11}{e['event_type']:<16}{e['decision']}")

    print(f"\n----- counters -----")
    granted = sum(e["decision"] == "ACCESS_GRANTED" for e in events)
    denied = sum(e["decision"] == "ACCESS_DENIED" for e in events)
    print(f"total scans: {len(events)}")
    print(f"granted: {granted}")
    print(f"denied: {denied}")
    print(f"asset scans: {len(events) - granted - denied}")
    for location in registry["readers"].values():
        print(f"scans at {location}: {sum(e['location'] == location for e in events)}")

    print(f"\n----- asset tracking: ASSET-007 history -----")
    for e in events:
        if e["entity_id"] == "ASSET-007":
            print(f"{e['timestamp']}  {e['location']:<6} ({e['reader_id']})")

    print(f"\nevents appended to {LOG_FILE}\n")
