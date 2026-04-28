import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None

def get_db():
    global supabase
    if supabase is None:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

def save_vitals(vitals: dict):
    try:
        db = get_db()
        db.table("patient_vitals").insert(vitals).execute()
        print(f"[DB] Saved vitals for {vitals['device_id']}")
    except Exception as e:
        print(f"[DB] Error saving vitals: {e}")

def get_latest_vitals():
    try:
        db = get_db()
        response = db.table("patient_vitals")\
            .select("*")\
            .order("timestamp", desc=True)\
            .limit(100)\
            .execute()
        return response.data
    except Exception as e:
        print(f"[DB] Error fetching vitals: {e}")
        return []

def get_vitals_by_device(device_id: str):
    try:
        db = get_db()
        response = db.table("patient_vitals")\
            .select("*")\
            .eq("device_id", device_id)\
            .order("timestamp", desc=True)\
            .limit(50)\
            .execute()
        return response.data
    except Exception as e:
        print(f"[DB] Error fetching vitals: {e}")
        return []