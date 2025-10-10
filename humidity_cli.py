import adafruit_dht
import board

# Initialize DHT22 once (outside loop)
# Use use_pulseio=False if on Pi (newer Adafruit library versions recommend it).

def get_dht_data():
    dht_sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    """Read temperature and humidity safely."""
    try:
        temperature = dht_sensor.temperature
        humidity = dht_sensor.humidity

        if humidity is not None and temperature is not None:
            dht_sensor.exit()
            dht_sensor=None
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
        dht_sensor=None
        time.sleep(2)
        return None, None

if __name__ == '__main__':
    temperature, humidity = get_dht_data()
