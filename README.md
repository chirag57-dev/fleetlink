# 🏥 FleetLink — Healthcare IoT Fleet Manager

A cloud-native SaaS platform for managing and monitoring a fleet of healthcare IoT devices in real time. Built with a full DevOps pipeline including CI/CD, Kubernetes orchestration, and observability.

🔗 **Live Demo:** https://fleetlink-topaz.vercel.app
📡 **API:** http://4.187.201.97:8000/docs

---

## 🎯 Problem Statement

In modern healthcare, medical devices (patient monitors, bed sensors, vital trackers) are deployed across multiple wards and clinics. Managing their status, pushing updates, and monitoring their health manually is inefficient and error-prone.

FleetLink solves this by providing a centralized command center for the entire device fleet.

---

## 🏗️ Architecture

10 Patient Simulators (Python)
↓ MQTT Protocol
Eclipse Mosquitto Broker (Docker/K8s)
↓
FastAPI Backend (Azure AKS)
↓
Supabase PostgreSQL Database
↓
Next.js Dashboard (Vercel) + Grafana Monitoring


---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| IoT Protocol | MQTT (Eclipse Mosquitto) | Device communication |
| Simulator | Python + paho-mqtt | 10 virtual patient beds |
| Backend | FastAPI (Python) | REST API + MQTT listener |
| Database | Supabase (PostgreSQL) | Vitals storage |
| Frontend | Next.js + Tailwind CSS | Real-time dashboard |
| Monitoring | Grafana + Prometheus | Observability |
| Containers | Docker | Application packaging |
| Orchestration | Kubernetes (Azure AKS) | Container management |
| CI/CD | GitHub Actions | Automated deployment |
| Registry | Azure Container Registry | Docker image storage |
| IaC | Terraform | Infrastructure provisioning |

---

## 🚀 DevOps Features

### CI/CD Pipeline
Every push to `master` triggers GitHub Actions which:
- Runs backend tests
- Builds Docker images
- Pushes to Azure Container Registry
- Deploys to AKS automatically

### Kubernetes Deployment
- Backend, MQTT Broker and Simulator all run as separate pods
- Auto-restart on crash via K8s liveness probes
- Horizontal scaling with single command

### Infrastructure as Code
- Entire Azure infrastructure provisioned via Terraform
- Reproducible in any environment with `terraform apply`

### Observability
- Prometheus scrapes metrics from backend every 15 seconds
- Grafana dashboard shows critical patients, normal patients, total fleet size
- Alerts configured for critical vital thresholds

### Chaos Engineering
- 5% random chance of critical readings per device
- Tests system alerting and resilience automatically

---

## 📊 Real-time Dashboard

- 10 patient beds across 3 wards (A, B, C)
- Live vitals: Heart Rate, SpO2, Temperature, Blood Pressure
- Battery level monitoring
- Critical alerts with pulsing red indicator
- Auto-refresh every 5 seconds

---

## 🏃 Running Locally

### Prerequisites
- Docker Desktop
- Python 3.11+
- Node.js 18+

### Setup

```bash
# Clone the repo
git clone https://github.com/chirag57-dev/fleetlink.git
cd fleetlink

# Create environment file
cp .env.example .env
# Fill in your Supabase credentials in .env

# Start MQTT broker
docker-compose up -d mosquitto

# Start backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Start simulator
cd simulator
python patient_simulator.py

# Start frontend
cd frontend
npm install
npm run dev
```

---

## ☁️ Cloud Deployment

### Azure AKS
```bash
# Login to Azure
az login

# Create resource group
az group create --name fleetlink-rg --location centralindia

# Create AKS cluster
az aks create --resource-group fleetlink-rg --name fleetlink-aks --node-count 1

# Deploy to Kubernetes
kubectl apply -f infra/k8s/deployment.yml
```

### Terraform
```bash
cd infra/terraform
terraform init
terraform apply
```

---

## 📈 Monitoring

Grafana dashboard available at `http://localhost:3001` (local) showing:
- Critical patients over time
- Total patients online
- Normal vs critical ratio

---

## 🔮 Future Improvements

- TLS encryption on MQTT
- Multi-tenancy (multiple hospitals)
- AI anomaly detection on vitals
- OTA firmware update pipeline
- Mobile app for doctors

---

## 👨‍💻 Author

**Chirag** — JECRC University, Jaipur
- GitHub: [@chirag57-dev](https://github.com/chirag57-dev)

---

## 📄 License

MIT License