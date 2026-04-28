from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading
from mqtt_handler import start_mqtt_listener
from database import get_latest_vitals, get_vitals_by_device

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start MQTT listener in background thread
    thread = threading.Thread(target=start_mqtt_listener, daemon=True)
    thread.start()
    print("[API] MQTT listener started in background")
    yield
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

@app.get("/")
def root():
    return {"message": "FleetLink API is running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/vitals")
def get_vitals():
    data = get_latest_vitals()
    return {"data": data, "count": len(data)}

@app.get("/vitals/{device_id}")
def get_device_vitals(device_id: str):
    data = get_vitals_by_device(device_id)
    return {"device_id": device_id, "data": data}