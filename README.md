

## 🚗 Predictive Accident Prevention and Automated Crash Recovery using BlackBox System for Cars

A smart IoT-based system designed to prevent road accidents and enable automated crash response. It integrates multiple sensors with a Raspberry Pi to detect anomalies in vehicle behavior, predict accidents, and initiate crash recovery using a BlackBox system.

---

### 🔧 Tech Stack & Components

* **Hardware**:

  * Raspberry Pi
  * MPU6050 (Accelerometer & Gyroscope)
  * DHT11 (Temperature & Humidity Sensor)
  * MQ2 (Gas Sensor)
  * IR Sensor
  * USB Camera / PiCam
* **Software**:

  * Python
  * ThingSpeak API (Data Logging & Monitoring)
  * SMTP (Email Alert System)
  * OpenCV (optional for image capture)
* **Communication**: Wi-Fi or GSM (optional)

---

### 🧠 Key Features

* 🛑 **Accident Detection**: Uses MPU6050 to detect sudden tilts, shocks, or crashes
* 🔥 **Fire/Gas Leak Detection**: MQ2 monitors potential fuel leaks post-accident
* 🌡️ **Environment Monitoring**: DHT11 reports in-cabin temperature and humidity
* 📸 **Automatic Image Capture**: Captures scene after crash for evidence
* 🚨 **Real-Time Alerts**: Sends email alerts with sensor data and image evidence
* 🗃️ **BlackBox Logging**: Stores historical data for accident analysis (ThingSpeak)

---

### 📂 Folder Structure

```
accident-blackbox/
├── sensors/
│   ├── mpu6050.py
│   ├── dht11.py
│   ├── mq2.py
│   └── ir_sensor.py
├── main.py
├── capture.py
├── alerts/
│   └── email_alert.py
├── cloud/
│   └── thingspeak_uploader.py
├── README.md
```

---

### 📦 Setup Instructions

1. **Connect hardware sensors** to Raspberry Pi GPIO pins

2. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/accident-blackbox.git
   cd accident-blackbox
   ```

3. **Install required Python libraries**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the main program**

   ```bash
   python3 main.py
   ```

---

### 📊 Data Visualization

* Sensor data is uploaded live to **ThingSpeak** dashboard
* Data like acceleration, gas levels, temperature, and crash flags are visualized
* Helps in post-accident investigation and pattern analysis

---

### 📘 Use Case

This project is designed to **reduce response time in accidents**, improve **driver safety**, and **log crash data** similar to aviation black boxes. Suitable for integration in smart vehicles and student research in IoT + AI for automotive safety.

