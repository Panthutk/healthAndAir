# 🌱 Health And Air Quality Monitoring System

This project integrates **Primary** and **Secondary** environmental data using Node-RED, MQTT, and HTTP APIs to store sensor data in a  database for real-time monitoring and analysis.

---

## 🚀 Project Overview

HealthandAir uses KidBright to collect real-time measurements of dust AQI, temperature, and humidity. To enhance accuracy, it also uses external data sources from aqicn.org and the tmd.go.th via API. The goal is to compare indoor and outdoor air conditions, helping users make decisions about whether to go outside or wear a mask for better health protection.

## 🔥 Project Feature

 🔧 Real-time Environmental Monitoring
Collects real-time data from various sources including:

* KidBright sensors (temperature, humidity, light, heartbeat, and sound)

* AQICN API (air quality data such as PM2.5, PM10, CO, O₃, etc.)

* TMD API (weather data like temperature, humidity, and rainfall)

🧠 Data Integration and Storage

* Integrates primary (local) and secondary (external) environmental data

* Stores all data in a MySQL database managed through phpMyAdmin

🌐 Node-RED Automation

* Automated flows for:

  * Fetching and injecting data every 60 minutes

  * Connecting to APIs and processing sensor input

  * Publishing/consuming via MQTT

📦 Flask + OpenAPI (Swagger) Backend

* RESTful API endpoints using Connexion

* Swagger UI to test and document APIs

📊 Interactive Dashboard

* Visualizes sensor and weather data using Plotly

* Dynamic graphs and tabs for each data source (KidBright, AQI, TMD)

* Built with HTML, Bootstrap, and JavaScript

---

## 📂 Project Structure

### 🔹 Primary Data (KidBright Sensor)

* Source: MQTT broker (`iot.cpe.ku.ac.th`)
* Topic: `b6610545421/sensors`
* Script: `./backend/kidbright.py`
* Collected metrics:
  * Temperature
  * Humidity
  * Light
  * AQI
  * Latitude / Longitude

### 🔹 Secondary Data (External APIs)

* Script: `./backend/nodeRed.json`

1. **AQICN API** – Air Quality at Kasetsart:
    * Pulls every 60 minutes using HTTP GET
    * Stores: AQI, PM2.5, PM10, CO, NO2, SO2, O3, temp, humidity, pressure, wind, UV, etc.
    * Location: `geo:13.8460;100.5650`

2. **TMD Weather API** – Thai Meteorological Department:
    * Pulls every 3 hours
    * Finds the closest station to fixed lat/lon (13.9192, 100.605)
    * Stores: Temperature, Humidity, Wind

---

## 🛠️ Requirements

* Python 3.5.2+

---

## ⚙️ Setup Instructions

### 📦 Python Environment

#### Create virtual environment

```powershell
python -m venv venv
```

#### Activate (Windows)

```powershell
.\venv\Scripts\activate
```

#### Install dependencies

```powershell
pip install -r requirements.txt
```

#### Run this command in repository terminal

```powershell
python app.py
```

#### In a seperate repository terminal run (Activate Virtual Environment)

```powershell
python -m http.server 8000
```

#### And open your browser to here

```powershell
http://localhost:8000
```

## Team Members

| Members                                                   | Photo                                                |
|---------------------------------------------------------------|--------------------------------------------------------|
| 66105455421 Panthut Ketphan            | <img src="member.jpg" width="200">   |
| 6610545332 Prima Xivivadh      | <img src="IMG_0046.png" width="200"> |
