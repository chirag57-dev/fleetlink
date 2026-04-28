from pydantic import BaseModel
from typing import Optional

class PatientVitals(BaseModel):
    device_id: str
    patient_name: str
    ward: str
    heart_rate: int
    spo2: int
    temperature: float
    systolic_bp: int
    battery: int
    status: str
    timestamp: str

class DeviceStatus(BaseModel):
    device_id: str
    status: str
    last_seen: str
    ward: str