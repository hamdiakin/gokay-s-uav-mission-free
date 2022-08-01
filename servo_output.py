# Import libraries
import RPi.GPIO as GPIO
from time import sleep


def run_servo():
    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    servo_pin = 12

    GPIO.setup(servo_pin, GPIO.OUT)
    servo1 = GPIO.PWM(servo_pin, 50)  # Note 11 is pin, 50 = 50Hz pulse

    # start PWM running, but with value of 0 (pulse off)
    servo1.start(0)

    for duty in range(0, 101, 1):
        servo1.ChangeDutyCycle(duty)  # provide duty cycle in the range 0-100
        sleep(0.01)


def stop_servo():
    GPIO.cleanup()
