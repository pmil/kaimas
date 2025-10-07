### Install DB

# System install
sudo apt update
sudo apt install influxdb influxdb-client -y
sudo systemctl enable influxdb
sudo systemctl start influxdb

# Install python lib
sudo apt install -y python3-influxdb-client

# Open with UI
http://<raspberrypi-ip>:8086

# Example code for connecting DB and setting data:
```
from prometheus_client import start_http_server, Gauge
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import adafruit_dht
import board
import time
import os

# ---- CONFIG ----
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "YOUR_INFLUXDB_TOKEN_HERE"
INFLUX_ORG = "kaimas"
INFLUX_BUCKET = "environment"
DHT_PIN = board.D4

# ---- Setup ----
dht_sensor = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)
dht_humidity = Gauge('adafruit_dht_humidity', 'Humidity (%)')
dht_temperature = Gauge('adafruit_dht_temperature', 'Temperature (Celsius)')

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def get_dht_data():
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity
        if humidity is not None and temperature is not None:
            return temperature, humidity
        else:
            print("DHT read failed: None values")
            return None, None
    except RuntimeError as error:
        print("RuntimeError:", error.args[0])
        return None, None
    except Exception as e:
        print("Unexpected error:", e)
        dht_sensor.exit()
        time.sleep(2)
        return None, None

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus metrics on :8000, logging to InfluxDB...")

    while True:
        temperature, humidity = get_dht_data()

        if temperature is not None and humidity is not None:
            # Update Prometheus metrics
            dht_temperature.set(temperature)
            dht_humidity.set(humidity)

            # Write to InfluxDB
            point = (
                Point("dht22")
                .tag("location", "indoor")
                .field("temperature", float(temperature))
                .field("humidity", float(humidity))
                .time(time.time_ns(), WritePrecision.NS)
            )
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
            print(f"Logged: Temp={temperature:0.1f}°C  Hum={humidity:0.1f}%")

        time.sleep(10)

```
