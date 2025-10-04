#!/bin/bash
# Usage: ./service_control.sh action.json

# Check input argument
if [ -z "$1" ]; then
    echo "Usage: $0 <json_file>"
    exit 1
fi

JSON_FILE="$1"

# Parse JSON
SERVICE=$(jq -r '.service' "$JSON_FILE")
ACTION=$(jq -r '.action' "$JSON_FILE")

# Validate parsed values
if [ -z "$SERVICE" ] || [ "$SERVICE" = "null" ]; then
    echo "Error: 'service' not found in JSON."
    exit 1
fi

if [ -z "$ACTION" ] || [ "$ACTION" = "null" ]; then
    echo "Error: 'action' not found in JSON."
    exit 1
fi

# Perform action
case "$ACTION" in
    start|stop|restart|status|enable|disable)
        echo "Executing: systemctl $ACTION $SERVICE"
        sudo systemctl "$ACTION" "$SERVICE"
        ;;
    *)
        echo "Error: Unsupported action '$ACTION'."
        echo "Supported actions: start, stop, restart, status, enable, disable"
        exit 1
        ;;
esac