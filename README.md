# kaimas

### User set
```
git config --global user.name "pmil"
git config --global user.email "paulius.milasauskas@gmail.com"
```

### Flash fresh pi
```
wget https://downloads.raspberrypi.org/raspios_lite_armhf_latest -O raspios_lite_latest.zip
sudo dd if=2025-05-13-raspios-bookworm-armhf-lite.img of=/dev/sda bs=4M status=progress conv=fsync
```

### Config raspi
sudo raspi-config

### Systemd commands
```
sudo systemctl daemon-reload
sudo apt-get install prometheus
sudo systemctl status dht.service
```

### Install tools



