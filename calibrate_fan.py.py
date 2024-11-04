#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys

# Configuration
FAN_PIN = 21            # BCM pin used to drive transistor's base
PWM_FREQ = 25           # [Hz]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)

# Initialize fan control
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
fan.start(0)

try:
    while True:
        try:
            # Prompt user for fan speed
            fanSpeed = float(input("Enter Fan Speed (0-100): "))

            # Validate the input is within the acceptable range
            if 0 <= fanSpeed <= 100:
                fan.ChangeDutyCycle(fanSpeed)
            else:
                print("Invalid input: Please enter a value between 0 and 100.")
        except ValueError:
            # Handle non-numeric input gracefully
            print("Invalid input: Please enter a numeric value.")

except KeyboardInterrupt:
    print("\nFan control interrupted by keyboard.")

finally:
    # Cleanup GPIO settings before exiting
    fan.stop()
    GPIO.cleanup()
    sys.exit()
