# copy services
sudo cp ./systemd/*.service /etc/systemd/system/
sudo cp ./systemd/*.timer /etc/systemd/system/

# create checksum file
sudo touch /var/lib/config-checksum
sudo chown pi:pi /var/lib/config-checksum
sudo chmod +x /home/pi/kaimas/git-pull.sh
sudo chmod +x /home/pi/kaimas/service_control.sh


# Run services
sudo systemctl daemon-reload
sudo systemctl enable dht.service
sudo systemctl restart dht.service
sudo systemctl restart prometheus.service
sudo systemctl restart pull-from-git.timer
sudo systemctl enable service-control.service