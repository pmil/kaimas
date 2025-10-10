from prometheus_client import start_http_server, Gauge
import time
import json
import os

# Prometheus metrics
dht_humidity = Gauge('adafruit_dht_humidity', 'Humidity (%)')
dht_temperature = Gauge('adafruit_dht_temperature', 'Temperature (Celsius)')

tmp_path = "/tmp/humidity.json.tmp"
final_path = "/tmp/humidity.json"

def get_dht_data():

    file_path = tmp_path
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus metrics available on port http://localhost:8000")

    while True:
        os.replace(final_path, tmp_path) 
        data = get_dht_data()
        temperature=data["temperature"]
        humidity=data["humidity"]
        if temperature is not None and humidity is not None:
            dht_temperature.set(temperature)
            dht_humidity.set(humidity)
            print(f"Temp={temperature}°C  Humidity={humidity}%")
        else:
            print("Skipping update due to read error")
         # atomic replace
        time.sleep(60)  # at least 2 seconds; 10 is safer
