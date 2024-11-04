# Pi PWM Fan Control

## Overview
This project provides a simple Python script to control a PWM fan on a Raspberry Pi, adjusting the fan speed based on the CPU temperature. The script allows for configurable temperature thresholds, fan speed steps, and more to help maintain an optimal operating temperature for your Raspberry Pi.

## Setup Instructions

### Step 1: Configure fan_control.py
Edit the `fan_control.py` file to adjust settings like the GPIO pin for fan control, speed, and temperature thresholds.

Key configuration variables:

```python
FAN_PIN = 21            # BCM pin used to drive transistor's base
WAIT_TIME = 1           # [s] Time to wait between each refresh
FAN_MIN = 40            # [%] Fan minimum speed.
PWM_FREQ = 25           # [Hz] Change this value if fan has strange behavior
```

#### Configurable Temperature and Fan Speed Steps
The fan speed will change according to the CPU temperature. You can configure these steps as follows:

```python
tempSteps = [40, 60]    # [°C] - Temperature thresholds for fan speed control
speedSteps = [0, 100]   # [%] - Corresponding fan speed for each temperature threshold
```
Ensure that each temperature step has a corresponding speed step, otherwise the script will not function correctly.

### Step 2: Install and Enable the Service (Optional)
If you prefer not to use the provided installation script, you can manually deploy the files and set up the service.

- **Copy `fan_control.py` to `/opt/fan_control.py`**

  ```bash
  sudo cp fan_control.py /opt/fan_control.py
  ```

- **Copy `fan.service` to `/etc/systemd/system/fan.service`**

  ```bash
  sudo cp fan.service /etc/systemd/system/fan.service
  ```

- **Reload the systemd daemon and enable the service**

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable fan.service
  sudo systemctl start fan.service
  ```

### Step 3: Verify Service Status
You can verify that the fan control service is running properly with the following command:

```bash
sudo systemctl status fan.service
```
This command will show you the status and logs for the fan control service. Make sure there are no errors.

## Notes
- The script must be run as root to access GPIO pins.
- Adjust `PWM_FREQ` if your fan exhibits unusual behavior, such as noise or inconsistent speed.
- Ensure that the `fan.service` file is configured correctly to point to `/opt/fan_control.py`.

### Example fan.service File
The `fan.service` file should look like this:

```ini
[Unit]
Description=PWM Fan Control Service
After=multi-user.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /opt/fan_control.py
Restart=always
RestartSec=5
TimeoutStartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=pwm_fan_control

[Install]
WantedBy=multi-user.target
```

## Troubleshooting
- **Service Not Starting:** Make sure you have copied the files to the correct locations and reloaded the `systemd` daemon.
- **Fan Not Spinning:** Double-check your wiring and ensure the GPIO pin and fan specifications match those configured in the script.

## Contributions
Feel free to fork this project and submit pull requests for new features, bug fixes, or improvements.

## License
This project is open source and available under the MIT License.

