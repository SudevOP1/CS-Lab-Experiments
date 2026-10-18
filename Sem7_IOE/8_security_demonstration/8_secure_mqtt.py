import json
import time
import threading
import jwt
import paho.mqtt.client as mqtt

BROKER = "localhost"
PLAIN_PORT = 1883
TLS_PORT = 8883
CA_FILE = "ca.crt"
USERNAME = "esp32"
PASSWORD = "esp32pass"
TOPIC = "ioe/security/sensor"
N_MESSAGES = 20

JWT_SECRET = "ioe-gateway-secret-key-change-this-in-production"

def connect(port, secure, username=None, password=None):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if secure:
        client.tls_set(ca_certs=CA_FILE)
    if username:
        client.username_pw_set(username, password)

    done = threading.Event()
    result = {}

    def on_connect(c, userdata, flags, reason_code, properties):
        result["rc"] = reason_code
        done.set()

    client.on_connect = on_connect

    start = time.perf_counter()
    try:
        client.connect(BROKER, port)
    except Exception as e:
        return None, f"connection error: {e}", 0
    client.loop_start()
    done.wait(5)
    connect_time = (time.perf_counter() - start) * 1000

    rc = result.get("rc")
    if rc is None or rc.is_failure:
        client.loop_stop()
        client.disconnect()
        return None, f"rejected: {rc}", connect_time
    return client, "connected", connect_time

def measure(port, secure, username=None, password=None):
    client, status, connect_time = connect(port, secure, username, password)
    print(f"  {status}")
    if client is None:
        return None

    latencies = []
    got = threading.Event()

    def on_message(c, userdata, msg):
        sent = json.loads(msg.payload)["t"]
        latencies.append((time.perf_counter() - sent) * 1000)
        if len(latencies) == N_MESSAGES:
            got.set()

    client.on_message = on_message
    client.subscribe(TOPIC, qos=1)
    time.sleep(0.5)

    start = time.perf_counter()
    for i in range(N_MESSAGES):
        payload = {"device": "ESP32", "protocol": "MQTTS" if secure else "MQTT",
                   "sensor": "MQ-2", "value": 400 + i, "t": time.perf_counter()}
        client.publish(TOPIC, json.dumps(payload), qos=1)
    got.wait(10)
    total = time.perf_counter() - start

    client.loop_stop()
    client.disconnect()

    return {
        "connect_ms": connect_time,
        "latency_ms": sum(latencies) / max(len(latencies), 1),
        "throughput": len(latencies) / total,
        "received": len(latencies),
    }

def issue_token(device, topics, expires_in):
    claims = {"sub": device, "topics": topics, "exp": int(time.time()) + expires_in}
    return jwt.encode(claims, JWT_SECRET, algorithm="HS256")

def gateway_authorize(token, topic):
    # application-layer gateway: validates jwt before forwarding to the broker
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False, "token expired"
    except jwt.InvalidTokenError:
        return False, "invalid token"
    if topic not in claims["topics"]:
        return False, f"{claims['sub']} not authorized for {topic}"
    return True, f"{claims['sub']} authorized"

if __name__ == "__main__":

    print(f"\n----- baseline mqtt (port {PLAIN_PORT}) -----")
    plain = measure(PLAIN_PORT, secure=False)

    print(f"\n----- mqtt over tls (port {TLS_PORT}) -----")
    secure = measure(TLS_PORT, secure=True, username=USERNAME, password=PASSWORD)

    if plain and secure:
        print(f"\n----- comparison -----")
        print(f"{'Parameter':<22}{'MQTT':>12}{'MQTT/TLS':>12}")
        print(f"{'connection time (ms)':<22}{plain['connect_ms']:>12.2f}{secure['connect_ms']:>12.2f}")
        print(f"{'avg latency (ms)':<22}{plain['latency_ms']:>12.2f}{secure['latency_ms']:>12.2f}")
        print(f"{'throughput (msg/s)':<22}{plain['throughput']:>12.2f}{secure['throughput']:>12.2f}")
        print(f"{'messages received':<22}{plain['received']:>12}{secure['received']:>12}")
        print(f"tls connection overhead: {secure['connect_ms'] - plain['connect_ms']:.2f} ms")

    print(f"\n----- security verification -----")
    tests = [
        ("tls + valid credentials", True, USERNAME, PASSWORD),
        ("tls + wrong password", True, USERNAME, "wrong"),
        ("tls + no credentials", True, None, None),
    ]
    for name, use_tls, user, pwd in tests:
        client, status, _ = connect(TLS_PORT, use_tls, user, pwd)
        if client:
            client.loop_stop()
            client.disconnect()
        print(f"{name:<26} -> {status}")

    print(f"\n----- jwt authentication (gateway layer) -----")
    valid = issue_token("ESP32", [TOPIC], expires_in=60)
    expired = issue_token("ESP32", [TOPIC], expires_in=-10)
    other = issue_token("ESP8266", ["ioe/other/sensor"], expires_in=60)
    tampered = valid[:-4] + "abcd"

    print(f"valid token: {valid}\n")
    for name, token in [("valid", valid), ("expired", expired), ("wrong topic", other), ("tampered", tampered)]:
        ok, reason = gateway_authorize(token, TOPIC)
        print(f"{name:<12} -> {'ACCEPTED' if ok else 'REJECTED'} ({reason})")
    print()
