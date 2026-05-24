import paho.mqtt.client as mqtt
import json
import time
import random
import threading
from config import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC_PREFIX, PATIENTS, PUBLISH_INTERVAL

# ── MQTT connection callbacks ──────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{userdata['id']}] Connected to MQTT Broker")
    else:
        print(f"[{userdata['id']}] Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"[{userdata['id']}] Disconnected. Reconnecting...")
    client.reconnect()

# ── Simulate realistic patient vitals ─────────────────────────────────────
def generate_vitals(patient):
    is_critical = random.random() < 0.05

    return {
        "device_id":    patient["id"],
        "patient_name": patient["name"],
        "ward":         patient["ward"],
        "heart_rate":   random.randint(140, 180) if is_critical else random.randint(60, 100),
        "spo2":         random.randint(85, 90)   if is_critical else random.randint(95, 100),
        "temperature":  round(random.uniform(38.5, 39.5) if is_critical else random.uniform(36.1, 37.5), 1),
        "systolic_bp":  random.randint(140, 180) if is_critical else random.randint(110, 130),
        "battery":      random.randint(20, 100),
        "status":       "critical" if is_critical else "normal",
        "timestamp":    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

# ── Per-patient thread ─────────────────────────────────────────────────────
def run_patient(patient):
    client = mqtt.Client(userdata=patient)
    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect

    # ── HiveMQ TLS + Auth ─────────────────────────────────────────────────
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.tls_set()

    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()

    topic = f"{MQTT_TOPIC_PREFIX}/{patient['id']}/telemetry"

    while True:
        vitals = generate_vitals(patient)
        payload = json.dumps(vitals)
        client.publish(topic, payload)
        print(f"[{patient['id']}] Ward {patient['ward']} → {vitals['status'].upper()} | HR: {vitals['heart_rate']} | SpO2: {vitals['spo2']}% | Temp: {vitals['temperature']}°C")
        time.sleep(PUBLISH_INTERVAL)

# ── Launch all 10 patients ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("🏥 FleetLink Simulator starting 10 patient beds...\n")
    threads = []

    for patient in PATIENTS:
        t = threading.Thread(target=run_patient, args=(patient,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.5)

    print(f"\n✅ All {len(PATIENTS)} patients online. Publishing every {PUBLISH_INTERVAL}s\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped.")