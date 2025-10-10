# copy services
sudo cp ./systemd/*.service /etc/systemd/system/
sudo cp ./systemd/*.timer /etc/systemd/system/
sudo cp service-controller.py /usr/local/bin/service-controller.py
sudo chmod 755 /usr/local/bin/service-controller.py

# create checksum file
sudo touch /var/lib/config-checksum
sudo chown pi:pi /var/lib/config-checksum

# Run services
sudo systemctl daemon-reload
sudo systemctl restart prometheus.service
sudo systemctl enable service-controller.timer
sudo systemctl start service-controller.timer
sudo systemctl enable zigbee2mqtt.service
sudo systemctl enable zigbee2mqtt.service
sudo systemctl enable dht-to-json.timer