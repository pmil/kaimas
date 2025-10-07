from prometheus_client import start_http_server, Gauge
import adafruit_dht
import board
import time

# Initialize DHT22 once (outside loop)
# Use use_pulseio=False if on Pi (newer Adafruit library versions recommend it).
dht_sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Prometheus metrics
dht_humidity = Gauge('adafruit_dht_humidity', 'Humidity (%)')
dht_temperature = Gauge('adafruit_dht_temperature', 'Temperature (Celsius)')

def get_dht_data():
    """Read temperature and humidity safely."""
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity

        if humidity is not None and temperature is not None:
            return temperature, humidity
        else:
            print("DHT read failed: None values")
            return None, None
    except RuntimeError as error:
        # Common DHT error, just retry next loop
        print("RuntimeError:", error.args[0])
        return None, None
    except Exception as e:
        # If something worse happens, reinitialize the sensor
        print("Unexpected error:", e)
        dht_sensor.exit()
        time.sleep(2)
        return None, None

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus metrics available on port http://localhost:8000")

    while True:
        temperature, humidity = get_dht_data()

        if temperature is not None and humidity is not None:
            dht_temperature.set(temperature)
            dht_humidity.set(humidity)
            print(f"Temp={temperature:0.1f}°C  Humidity={humidity:0.1f}%")
        else:
            print("Skipping update due to read error")

        time.sleep(10)  # at least 2 seconds; 10 is safer
