# Pi PWN fan control
## Edit the fan_control.py file to set the fan speed and temperature thresholds and the control pin


FAN_PIN = 21            # BCM pin used to drive transistor's base
WAIT_TIME = 1           # [s] Time to wait between each refresh
FAN_MIN = 40            # [%] Fan minimum speed.
PWM_FREQ = 25           # [Hz] Change this value if fan has strange behavior

### Configurable temperature and fan speed steps
tempSteps = [40, 60]    # [°C]
speedSteps = [0, 100]   # [%]

Copy fan_control.py to /opt/fan_control.py
Copy fan.service to /etc/systemd/system/fan.service