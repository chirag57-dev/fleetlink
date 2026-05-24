import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from database import save_vitals

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
TOPIC = "fleetlink/patients/#"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected to broker")
        client.subscribe(TOPIC)
        print(f"[MQTT] Subscribed to {TOPIC}")
    else:
        print(f"[MQTT] Connection failed: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[MQTT] Received from {payload['device_id']} | Status: {payload['status'].upper()}")
        save_vitals(payload)
    except Exception as e:
        print(f"[MQTT] Error processing message: {e}")

def start_mqtt_listener():
    client = mqtt.Client()
    
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.tls_set()
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()