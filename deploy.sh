sudo cp ./systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart dht.service
sudo systemctl restart prometheus.service
sudo systemctl enable --now config-update.timer