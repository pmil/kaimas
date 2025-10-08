#!/usr/bin/env python3
import subprocess
import yaml
import urllib.request
import os

# URL of your YAML file in Git
YAML_URL = "https://github.com/pmil/kaimas/raw/refs/heads/dev/config.yaml"
LOCAL_YAML = "/tmp/config.yaml"

# Download the YAML file
urllib.request.urlretrieve(YAML_URL, LOCAL_YAML)

# Read the YAML
with open(LOCAL_YAML, "r") as f:
    services = yaml.safe_load(f)

# Example YAML structure:
# - name: ssh
#   action: restart
# - name: nginx
#   action: stop
# - name: apache2
#   action: start

for svc in services:
    name = svc["name"]
    action = svc["action"]
    print(f"Executing: systemctl {action} {name}")
    subprocess.run(["sudo", "systemctl", action, name])
