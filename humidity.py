from prometheus_client import start_http_server, Gauge
import adafruit_dht
import board
import time

def get_dht_data():
    dht_data = []

    dht = adafruit_dht.DHT22(board.D4)
    try:
        temperature = dht.temperature
        humidity = dht.humidity
    except RuntimeError as error:
        print(error.args[0])

    if humidity is not None and temperature is not None:
        # print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        dht_data=[temperature, humidity]
    else:
        print("Failed to retrieve data from humidity sensor")
    return dht_data

def process_request(t):
    time.sleep(t)

if __name__ == '__main__':
    adafruit_dht_humidity = Gauge('adafruit_dht_humidity','humidity')
    adafruit_dht_temperature = Gauge('adafruit_dht_temperature','temperature')
    start_http_server(8000)

    while True:
        # Get DHT data
        dht_data = get_dht_data()
        adafruit_dht_temperature.set(dht_data[0])
        adafruit_dht_humidity.set(dht_data[1])
        process_request(30)
