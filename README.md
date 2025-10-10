# kaimas

### Flash fresh pi
```
wget https://downloads.raspberrypi.org/raspios_lite_armhf_latest -O raspios_lite_latest.zip
sudo dd if=2025-05-13-raspios-bookworm-armhf-lite.img of=/dev/sda bs=4M status=progress conv=fsync
```

### Create secrets.env file
```
PROM_USERNAME=prom_userName
PROM_PASSWORD=prom_password
```

### Config raspi
```
sudo raspi-config
mkdir /home/pi/prometheus
mkdir /home/pi/prometheus/data

```

### Install tools
```
sudo apt update
sudo apt upgrade
sudo apt-get install git
sudo apt-get install prometheus
sudo apt install -y mosquitto mosquitto-clients
sudo apt-get install git nodejs npm
sudo apt install prometheus-node-exporter
```

### Python libs
```
sudo apt install -y python3-yaml
sudo apt install -y python3-prometheus-client
sudo apt install -y python3-paho-mqtt
python3 -m pip install adafruit-circuitpython-dht --break-system-packages
```

### User set
```
git config --global user.name "pmil"
git config --global user.email "paulius.milasauskas@gmail.com"
```

### Systemd commands
```
sudo systemctl daemon-reload
sudo apt-get install prometheus
sudo systemctl status dht.service
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

### Test mosquitto
mosquitto_sub -v -t '#'
mosquitto_pub -h localhost -t "zigbee2mqtt/Cam/set" -m '{"state": "OFF"}'

### Read data from localhost
curl -v http://localhost:8000

### Zigbee
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git
sudo npm install -g pnpm


## Links
# Node RED
https://nodered.org/docs/getting-started/raspberrypi




# Prometheus to read from file
sudo nano /lib/systemd/system/prometheus-node-exporter.service
ExecStart=/usr/bin/prometheus-node-exporter \
  --collector.textfile.directory=/home/pi/node_exporter
sudo systemctl status prometheus-node-exporter.service


# Install influxdb
wget -q https://repos.influxdata.com/influxdata-archive.key
echo "deb [signed-by=/usr/share/keyrings/influxdata-archive.key] https://repos.influxdata.com/debian stable main" | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt update
sudo apt install influxdb2 -y
