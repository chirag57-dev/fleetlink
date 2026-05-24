import paho.mqtt.client as mqtt
import json
import time
import random
import threading
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC_PREFIX = "fleetlink/patients"
PUBLISH_INTERVAL = 5

PATIENTS = [
    {"id": "BED_001", "name": "Rahul Sharma",    "ward": "A"},
    {"id": "BED_002", "name": "Priya Verma",     "ward": "A"},
    {"id": "BED_003", "name": "Amit Patel",      "ward": "A"},
    {"id": "BED_004", "name": "Sneha Gupta",     "ward": "B"},
    {"id": "BED_005", "name": "Rohit Singh",     "ward": "B"},
    {"id": "BED_006", "name": "Anjali Mehta",    "ward": "B"},
    {"id": "BED_007", "name": "Vikram Joshi",    "ward": "C"},
    {"id": "BED_008", "name": "Neha Agarwal",    "ward": "C"},
    {"id": "BED_009", "name": "Suresh Kumar",    "ward": "C"},
    {"id": "BED_010", "name": "Kavita Reddy",    "ward": "C"},
]

simulator_running = False
simulator_threads = []

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

def run_patient(patient):
    client = mqtt.Client(userdata=patient)

    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.tls_set()

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_start()
        topic = f"{MQTT_TOPIC_PREFIX}/{patient['id']}/telemetry"

        while simulator_running:
            vitals = generate_vitals(patient)
            client.publish(topic, json.dumps(vitals))
            print(f"[SIM] {patient['id']} → {vitals['status'].upper()} | HR: {vitals['heart_rate']}")
            time.sleep(PUBLISH_INTERVAL)
    except Exception as e:
        print(f"[SIM] Error for {patient['id']}: {e}")

def start_simulator():
    global simulator_running, simulator_threads

    if simulator_running:
        return False

    simulator_running = True
    simulator_threads = []

    for patient in PATIENTS:
        t = threading.Thread(target=run_patient, args=(patient,), daemon=True)
        t.start()
        simulator_threads.append(t)

    print(f"[SIM] Started {len(PATIENTS)} patient simulators")
    return True

def stop_simulator():
    global simulator_running
    simulator_running = False
    print("[SIM] Stopped simulator")

def is_running():
    return simulator_running