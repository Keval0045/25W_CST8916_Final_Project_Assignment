import random
import time
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message
import json

CONNECTION_STRING = "HostName=SkatewayIoTHub.azure-devices.net;DeviceId=sensor-simulator;SharedAccessKey=shRrDP+2e4tJXCI87zVSz9zz3CQxw6ql8i/K/YKW6g8="

LOCATIONS = ["Dow's Lake", "Fifth Avenue", "NAC"]

def generate_sensor_data():
    return {
        "location": random.choice(LOCATIONS),
        "iceThickness": random.randint(20, 35),
        "surfaceTemperature": round(random.uniform(-10, 0), 1),
        "snowAccumulation": random.randint(0, 15),
        "externalTemperature": round(random.uniform(-15, 5), 1),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    client.connect()
    print("Connected to IoT Hub")

    while True:
        data = generate_sensor_data()
        json_data = json.dumps(data)
        msg = Message(json_data)
        client.send_message(msg)
        print("Sent:", json_data)
        time.sleep(10)

if __name__ == "__main__":
    main()
