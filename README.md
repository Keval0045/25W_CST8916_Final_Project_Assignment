# 25W_CST8916_Final_Project_Assignment

Absolutely! Here's a polished and detailed `README.md` structured exactly according to your evaluation rubric:

---

#  Rideau Canal Skateway – Real-Time Monitoring System

## Scenario Description

The **Rideau Canal Skateway** in Ottawa is the world’s largest naturally frozen skating rink. Its safety and maintenance depend heavily on real-time environmental data like ice thickness, surface conditions, and weather.

To help the **National Capital Commission (NCC)** monitor the skateway efficiently, this project implements a **real-time IoT-based monitoring system** using Azure services. The system simulates sensors, streams data through Azure IoT Hub, processes it via Azure Stream Analytics, and stores results in Azure Blob Storage for analysis.

---

## System Architecture

###  Architecture Diagram

```
Simulated IoT Sensors (Python Script)
        ↓
   Azure IoT Hub (iotinput)
        ↓
Azure Stream Analytics
        ↓
Azure Blob Storage (bloboutput in JSON format)
```

This flow enables near real-time visibility into conditions across multiple canal locations (e.g., Dow’s Lake, Fifth Avenue, NAC).

---

##  Implementation Details

### IoT Sensor Simulation

- **Sensor Locations**:
  - Dow's Lake
  - Fifth Avenue
  - National Arts Centre (NAC)

- **Generated Metrics** every 10 seconds:
  - `iceThickness` (cm)
  - `surfaceTemperature` (°C)
  - `snowAccumulation` (cm)
  - `externalTemperature` (°C)
  - `timestamp` (ISO 8601)

#### Payload Example:

```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2024-11-23T12:00:00Z"
}
```

- Script uses **`paho-mqtt`** and **`azure-iot-device`** to push data to Azure IoT Hub.
- Located under `sensor-simulation/simulate_sensors.py`.

---

###  Azure IoT Hub Configuration

- Created IoT Hub in Azure Portal.
- Registered device (e.g., `skateway-sensor`) and retrieved device connection string.
- Default message routing enabled (`messages/events`).
- Used device connection string in simulation script to send data.

---

### Azure Stream Analytics

- **Job Input**: `iotinput` (from IoT Hub)
- **Job Output**: `bloboutput` (to Blob Storage)
- **SQL Query**:

```sql
SELECT
    System.Timestamp AS windowEnd,
    location,
    AVG(CAST(iceThickness AS float)) AS avgIceThickness,
    MAX(CAST(snowAccumulation AS bigint)) AS maxSnowAccumulation
INTO
    bloboutput
FROM
    iotinput
TIMESTAMP BY CAST(timestamp AS datetime)
GROUP BY
    TumblingWindow(minute, 5), location
```

- Processes data every 5 minutes, grouped by location.

---

### Azure Blob Storage

- Created a storage account and container (e.g., `skateway-results`).
- Stream Analytics output sends results here in JSON format.
- Organized by path: `data/{date}/{time}/filename.json`.

#### Sample Output File:

```json
{
  "windowEnd": "2025-04-05T12:05:00Z",
  "location": "Dow's Lake",
  "avgIceThickness": 26.5,
  "maxSnowAccumulation": 10
}
```

---

## Usage Instructions

### Running the Sensor Simulation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/25W_CST8916_Final_Project_Assignment.git
   cd 25W_CST8916_Final_Project_Assignment/sensor-simulation
   ```

2. Install required Python packages:
   ```bash
   pip install paho-mqtt azure-iot-device
   ```

3. Add your **device connection string** in `simulate_sensors.py`.

4. Run the script:
   ```bash
   python simulate_sensors.py
   ```

---

###  Configuring Azure Services

#### Azure IoT Hub
- Create IoT Hub in Azure
- Add device
- Copy device connection string to your script

#### Azure Stream Analytics
- Create job with:
  - **Input** from IoT Hub (`iotinput`)
  - **Output** to Blob Storage (`bloboutput`)
  - Use provided SQL query
- Start job to begin streaming

#### Azure Blob Storage
- Create storage account and container
- Connect as output from Stream Analytics job
- Set path pattern to organize files by date/time

---

## Results

### Aggregated Output Sample

```json
{
  "windowEnd": "2025-04-05T13:10:00Z",
  "location": "Fifth Avenue",
  "avgIceThickness": 24.7,
  "maxSnowAccumulation": 9
}
```

### Key Findings:
- Real-time analytics can detect when ice becomes too thin or snow levels are too high.
- Enables authorities to act quickly and ensure public safety.

---

## Reflection

### Challenges Faced
- Initial issues with Stream Analytics query due to incorrect field types and syntax.
- Timestamps needed explicit parsing to avoid aggregation errors.
- Azure service naming and linking (e.g., matching aliases) required attention.

### Solutions
- Used `CAST()` on numeric fields.
- Verified message format with Stream Analytics test features.
- Followed Azure documentation closely for job configuration.

---

##  Screenshots

- Azure IoT Hub setup
- Stream Analytics job configuration
- Output files in Blob Storage

 Stored under `/screenshots/`

---

## Repository Structure

```
25W_CST8916_Final_Project_Assignment/
├── README.md
├── sensor-simulation/
│   └── simulate_sensors.py
├── screenshots/
│   ├── iot-hub.png
│   ├── stream-analytics.png
│   └── blob-storage.png
```

---

## Author

**Keval Trivedi 041167761**  
