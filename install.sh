#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Variables
FAN_SCRIPT="fan_control.py"
SERVICE_FILE="fan.service"
INSTALL_DIR="/opt"
SERVICE_DIR="/etc/systemd/system"

# Ensure the script and service file exist in the current directory
if [ ! -f "$FAN_SCRIPT" ] || [ ! -f "$SERVICE_FILE" ]; then
    echo "Both $FAN_SCRIPT and $SERVICE_FILE must exist in the current directory." >&2
    exit 1
fi

# Make files executable
chmod +x "$FAN_SCRIPT"

# Copy fan_control.py to /opt
echo "Copying $FAN_SCRIPT to $INSTALL_DIR"
cp "$FAN_SCRIPT" "$INSTALL_DIR/$FAN_SCRIPT"

# Copy fan.service to /etc/systemd/system
echo "Copying $SERVICE_FILE to $SERVICE_DIR"
cp "$SERVICE_FILE" "$SERVICE_DIR/$SERVICE_FILE"

# Reload systemd daemon
echo "Reloading systemd daemon"
systemctl daemon-reload

echo "Script executed successfully."