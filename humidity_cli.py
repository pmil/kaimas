import adafruit_dht
import board
import time

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

if __name__ == '__main__':
    data = get_dht_data()
    write_to_json(data)
