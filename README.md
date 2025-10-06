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
```

### Install tools
```
sudo apt update
sudo apt upgrade
sudo apt-get install git
sudo apt-get install prometheus
sudo apt install -y mosquitto mosquitto-clients
sudo apt-get install git nodejs npm
```

### Python libs
```
sudo apt install -y python3-yaml
sudo apt install -y python3-prometheus-client
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

### Read data from localhost
curl -v http://localhost:8000

### Zigbee
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git
sudo npm install -g pnpm




