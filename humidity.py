from prometheus_client import start_http_server, Gauge
import time
import json

# Prometheus metrics
dht_humidity = Gauge('adafruit_dht_humidity', 'Humidity (%)')
dht_temperature = Gauge('adafruit_dht_temperature', 'Temperature (Celsius)')

def get_dht_data():
    file_path = "/tmp/humidity.json"
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus metrics available on port http://localhost:8000")

    while True:
        data = get_dht_data()

        if data["temperature"] is not None and data["humidity"] is not None:
            dht_temperature.set(data["temperature"])
            dht_humidity.set(data["humidity"])
            print(f"Temp={data[\"temperature\"]}°C  Humidity={data[\"humidity\"]}%")
        else:
            print("Skipping update due to read error")
        time.sleep(60)  # at least 2 seconds; 10 is safer
