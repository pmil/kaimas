#!/usr/bin/env python3
import yaml
import paho.mqtt.publish as publish
import os

# Configuration
CONFIG_FILE = "/home/pi/kaimas/controller.yaml"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

def read_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def send_device_state(name, state):
    topic = f"zigbee2mqtt/{name}/set"
    payload = f'{{"state":"{state}"}}'
    publish.single(topic, payload, hostname=MQTT_BROKER, port=MQTT_PORT)
    print(f"Sent {payload} to {topic}")

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file not found: {CONFIG_FILE}")
        return

    try:
        config = read_yaml(CONFIG_FILE)
        for item in config:
            name = item.get("name")
            state = item.get("state")
            if name and state:
                send_device_state(name, state)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
