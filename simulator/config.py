import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC_PREFIX = "fleetlink/patients"

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

PUBLISH_INTERVAL = 5