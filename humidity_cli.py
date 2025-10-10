import adafruit_dht
import board
import time
import json

def get_dht_data():
    SENSOR = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    """Read temperature and humidity safely."""
    try:
        temperature = SENSOR.temperature
        humidity = SENSOR.humidity

        if humidity is not None and temperature is not None:
            SENSOR.exit()
            SENSOR=None
            return {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
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
        SENSOR.exit()
        SENSOR=None
        time.sleep(2)
        return None, None

def write_to_json(data, path="/tmp/humidity.json"):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data written to {path}: {data}")
    except Exception as e:
        print(f"Error writing to {path}: {e}")

def write_to_prom(data, filepath):
    temperature = data["temperature"]
    humidity = data["humidity"]
    timestamp = data["timestamp"]
    with open(filepath, "w") as f:
        f.write(f"# HELP dht_temperature_celsius Temperature in Celsius\n")
        f.write(f"# TYPE dht_temperature_celsius gauge\n")
        f.write(f"dht_temperature_celsius {temperature:.2f}\n")
        f.write(f"# HELP dht_humidity_percent Relative humidity in percent\n")
        f.write(f"# TYPE dht_humidity_percent gauge\n")
        f.write(f"dht_humidity_percent {humidity:.2f}\n")
        f.write(f"# HELP dht_last_timestamp Timestamp\n")
        f.write(f"# TYPE dht_last_timestamp gauge\n")
        f.write(f"dht_last_timestamp {timestamp:.2f}\n")

if __name__ == '__main__':
    data = get_dht_data()
    write_to_json(data)
    write_to_prom(data,'/home/pi/node_exporter/humidity.prom')
