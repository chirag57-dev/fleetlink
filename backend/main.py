from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge, Counter
import threading
from mqtt_handler import start_mqtt_listener
from database import get_latest_vitals, get_vitals_by_device
import simulator as sim

# ── Prometheus Custom Metrics ──────────────────────────────────────────────
critical_patients = Gauge("fleetlink_critical_patients", "Number of critical patients")
normal_patients = Gauge("fleetlink_normal_patients", "Number of normal patients")
total_patients = Gauge("fleetlink_total_patients", "Total number of patients online")
mqtt_messages = Counter("fleetlink_mqtt_messages_total", "Total MQTT messages received")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start MQTT listener
    thread = threading.Thread(target=start_mqtt_listener, daemon=True)
    thread.start()
    print("[API] MQTT listener started")
    
    # Auto start simulator on startup
    sim.start_simulator()
    print("[API] Simulator auto-started")
    
    yield
    
    sim.stop_simulator()
    print("[API] Shutting down")

app = FastAPI(
    title="FleetLink API",
    description="Healthcare IoT Fleet Manager",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "FleetLink API is running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "simulator": sim.is_running()}

@app.get("/start-simulator")
def start_simulator():
    started = sim.start_simulator()
    return {"message": "Simulator started" if started else "Already running", "running": True}

@app.get("/simulator-status")
def simulator_status():
    return {"running": sim.is_running()}

@app.get("/vitals")
def get_vitals():
    data = get_latest_vitals()
    critical = len([d for d in data if d.get("status") == "critical"])
    normal = len([d for d in data if d.get("status") == "normal"])
    critical_patients.set(critical)
    normal_patients.set(normal)
    total_patients.set(len(data))
    mqtt_messages.inc()
    return {"data": data, "count": len(data)}

@app.get("/vitals/{device_id}")
def get_device_vitals(device_id: str):
    data = get_vitals_by_device(device_id)
    return {"device_id": device_id, "data": data}