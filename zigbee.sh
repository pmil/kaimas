# Install required apps
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g typescript

# Test mosquitto
mosquitto_sub -v -t '#'
tsc --version

# Go to home dir and clone repo
cd ~
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git
cd zigbee2mqtt/
pnpm install
pnpm build

sudo systemctl start zigbee2mqtt
sudo systemctl enable zigbee2mqtt
