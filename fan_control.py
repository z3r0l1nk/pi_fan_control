#!/usr/bin/python3
# -*- coding: utf-8 -*-

###################
###     V.2     ###
###################


import RPi.GPIO as GPIO
import time
import sys

# Configuration
FAN_PIN = 21            # BCM pin used to drive transistor's base
WAIT_TIME = 1           # [s] Time to wait between each refresh
FAN_MIN = 40            # [%] Fan minimum speed.
PWM_FREQ = 25           # [Hz] Change this value if fan has strange behavior

# Configurable temperature and fan speed steps
tempSteps = [40, 60]    # [°C]
speedSteps = [0, 100]   # [%]

# Fan speed will change only if the difference of temperature is higher than hysteresis
hyst = 1

# Setup GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
fan.start(0)

fanSpeedOld = 0

# We must set a speed value for each temperature step
if len(speedSteps) != len(tempSteps):
    print("Numbers of temp steps and speed steps are different")
    sys.exit(1)

def read_cpu_temp():
    """Reads the CPU temperature from the system file."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as cpuTempFile:
            cpuTemp = float(cpuTempFile.read()) / 1000
        return cpuTemp
    except FileNotFoundError:
        print("Error: CPU temperature file not found.")
        sys.exit(1)

def calculate_fan_speed(cpuTemp):
    """Calculates the fan speed based on the current CPU temperature."""
    if cpuTemp < tempSteps[0]:
        return speedSteps[0]
    elif cpuTemp >= tempSteps[-1]:
        return speedSteps[-1]
    else:
        for i in range(len(tempSteps) - 1):
            if tempSteps[i] <= cpuTemp < tempSteps[i + 1]:
                return round(
                    (speedSteps[i + 1] - speedSteps[i]) /
                    (tempSteps[i + 1] - tempSteps[i]) *
                    (cpuTemp - tempSteps[i]) +
                    speedSteps[i], 1
                )

try:
    while True:
        # Read CPU temperature
        cpuTemp = read_cpu_temp()

        # Calculate desired fan speed
        if abs(cpuTemp - fanSpeedOld) > hyst:
            fanSpeed = calculate_fan_speed(cpuTemp)

            # Only update if the fan speed has meaningfully changed
            if fanSpeed != fanSpeedOld and (fanSpeed >= FAN_MIN or fanSpeed == 0):
                fan.ChangeDutyCycle(fanSpeed)
                fanSpeedOld = fanSpeed

        # Wait until next refresh
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    print("Fan control interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()

except Exception as e:
    print(f"An error occurred: {e}")
    GPIO.cleanup()
    sys.exit(1)
