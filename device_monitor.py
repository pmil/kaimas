#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from prometheus_client import start_http_server, Gauge
import subprocess
import yaml
import time
import threading

# --- CONFIG ---
MQTT_BROKER = "localhost"
MQTT_TOPIC = "zigbee2mqtt/#"  # subscribe to all Zigbee2MQTT devices
METRICS_PORT = 9101  # Prometheus metrics port

# --- PROMETHEUS METRICS ---
device_state_metric = Gauge('device_state', 'Device ON/OFF state from MQTT', ['device_name'])

# --- STATE STORAGE ---
device_states = {}

# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = yaml.safe_load(msg.payload.decode())
        topic_parts = msg.topic.split('/')
        if len(topic_parts) >= 2:
            device_name = topic_parts[1]
            if isinstance(payload, dict) and 'state' in payload:
                state = payload['state']
                device_states[device_name] = state
                device_state_metric.labels(device_name=device_name).set(1 if state == 'ON' else 0)
                print(f"Updated {device_name} → {state}")
                handle_device_logic(device_name, state)
    except Exception as e:
        print("Error processing message:", e)

# --- CUSTOM LOGIC ---
def handle_device_logic(device_name, state):
    """
    Example: control local services based on MQTT device state.
    """
    if device_name.lower() == "cam":
        if state == "ON":
            subprocess.run(["systemctl", "start", "cam.service"])
        else:
            subprocess.run(["systemctl", "stop", "cam.service"])

# --- MQTT CLIENT THREAD ---
def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

# --- MAIN ---
if __name__ == "__main__":
    start_http_server(METRICS_PORT)
    threading.Thread(target=mqtt_thread, daemon=True).start()
    print(f"Prometheus metrics available at :{METRICS_PORT}/metrics")
    while True:
        time.sleep(10)
