"use client";
import { useEffect, useState } from "react";
import axios from "axios";

interface Vitals {
  device_id: string;
  patient_name: string;
  ward: string;
  heart_rate: number;
  spo2: number;
  temperature: number;
  systolic_bp: number;
  battery: number;
  status: string;
  timestamp: string;
}

export default function Home() {
  const [vitals, setVitals] = useState<Vitals[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<string>("");

  const fetchVitals = async () => {
    try {
      const res = await axios.get("http://localhost:8000/vitals");
      const data: Vitals[] = res.data.data;

      // Keep only latest reading per device
      const latest = Object.values(
        data.reduce((acc: Record<string, Vitals>, v) => {
          if (!acc[v.device_id] || v.timestamp > acc[v.device_id].timestamp) {
            acc[v.device_id] = v;
          }
          return acc;
        }, {})
      );

      setVitals(latest);
      setLastUpdated(new Date().toLocaleTimeString());
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch vitals", err);
    }
  };

  useEffect(() => {
    fetchVitals();
    const interval = setInterval(fetchVitals, 5000);
    return () => clearInterval(interval);
  }, []);

  const critical = vitals.filter((v) => v.status === "critical");
  const normal = vitals.filter((v) => v.status === "normal");

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-green-400">🏥 FleetLink</h1>
        <p className="text-gray-400 mt-1">Healthcare IoT Fleet Manager</p>
        <div className="flex gap-6 mt-4">
          <div className="bg-gray-800 rounded-lg px-4 py-2">
            <p className="text-xs text-gray-400">Total Patients</p>
            <p className="text-2xl font-bold text-white">{vitals.length}</p>
          </div>
          <div className="bg-red-900 rounded-lg px-4 py-2">
            <p className="text-xs text-red-300">Critical</p>
            <p className="text-2xl font-bold text-red-400">{critical.length}</p>
          </div>
          <div className="bg-green-900 rounded-lg px-4 py-2">
            <p className="text-xs text-green-300">Normal</p>
            <p className="text-2xl font-bold text-green-400">{normal.length}</p>
          </div>
          <div className="bg-gray-800 rounded-lg px-4 py-2">
            <p className="text-xs text-gray-400">Last Updated</p>
            <p className="text-sm font-bold text-white">{lastUpdated}</p>
          </div>
        </div>
      </div>

      {/* Patient Grid */}
      {loading ? (
        <p className="text-gray-400">Loading patient data...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {vitals
            .sort((a, b) => a.device_id.localeCompare(b.device_id))
            .map((v) => (
              <div
                key={v.device_id}
                className={`rounded-xl p-4 border ${
                  v.status === "critical"
                    ? "bg-red-950 border-red-500 shadow-red-500/20 shadow-lg"
                    : "bg-gray-800 border-gray-700"
                }`}
              >
                {/* Card Header */}
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <p className="font-bold text-white">{v.device_id}</p>
                    <p className="text-xs text-gray-400">{v.patient_name}</p>
                    <p className="text-xs text-gray-500">Ward {v.ward}</p>
                  </div>
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-bold ${
                      v.status === "critical"
                        ? "bg-red-500 text-white animate-pulse"
                        : "bg-green-800 text-green-300"
                    }`}
                  >
                    {v.status.toUpperCase()}
                  </span>
                </div>

                {/* Vitals Grid */}
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div className="bg-gray-900 rounded-lg p-2">
                    <p className="text-xs text-gray-500">Heart Rate</p>
                    <p className={`text-lg font-bold ${v.heart_rate > 120 ? "text-red-400" : "text-pink-400"}`}>
                      {v.heart_rate} <span className="text-xs">bpm</span>
                    </p>
                  </div>
                  <div className="bg-gray-900 rounded-lg p-2">
                    <p className="text-xs text-gray-500">SpO2</p>
                    <p className={`text-lg font-bold ${v.spo2 < 92 ? "text-red-400" : "text-blue-400"}`}>
                      {v.spo2}<span className="text-xs">%</span>
                    </p>
                  </div>
                  <div className="bg-gray-900 rounded-lg p-2">
                    <p className="text-xs text-gray-500">Temperature</p>
                    <p className={`text-lg font-bold ${v.temperature > 38 ? "text-red-400" : "text-orange-400"}`}>
                      {v.temperature}<span className="text-xs">°C</span>
                    </p>
                  </div>
                  <div className="bg-gray-900 rounded-lg p-2">
                    <p className="text-xs text-gray-500">Blood Pressure</p>
                    <p className="text-lg font-bold text-purple-400">
                      {v.systolic_bp}<span className="text-xs">mmHg</span>
                    </p>
                  </div>
                </div>

                {/* Battery */}
                <div className="mt-3">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Battery</span>
                    <span>{v.battery}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full ${
                        v.battery < 30 ? "bg-red-500" : "bg-green-500"
                      }`}
                      style={{ width: `${v.battery}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
        </div>
      )}
    </main>
  );
}