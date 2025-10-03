#!/usr/bin/env python3
import os
import subprocess
import hashlib
import yaml

REPO_DIR = "/home/pi/kaimas"
CONFIG_FILE = os.path.join(REPO_DIR, "config.yaml")
STATE_FILE = "/var/lib/config-checksum"

def get_file_hash(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # git pull
    subprocess.run(["git", "-C", REPO_DIR, "pull", "origin", "main"], check=True)

    new_hash = get_file_hash(CONFIG_FILE)
    old_hash = None
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            old_hash = f.read().strip()

    if new_hash != old_hash:
        print("Config changed, applying actions...")
        with open(CONFIG_FILE) as f:
            cfg = yaml.safe_load(f)

        for entry in cfg.get("services", []):
            name = entry.get("name")
            action = entry.get("action")
            if name and action:
                try:
                    run_cmd(["systemctl", action, name])
                except subprocess.CalledProcessError as e:
                    print(f"Failed: {e}")

        with open(STATE_FILE, "w") as f:
            f.write(new_hash)
    else:
        print("No changes in config.")

if __name__ == "__main__":
    main()
