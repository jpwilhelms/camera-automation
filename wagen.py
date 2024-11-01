import time
import signal
import sys
from gpiozero import Button
from gpiozero import DigitalInputDevice
from gpiozero import Motor

buttonRight = Button(26)
buttonLeft = Button(12)
flyingFish = DigitalInputDevice(23)
motor = Motor( forward=5, backward=6 )

def cleanup():
    print("Räume auf...")
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

signal.signal(signal.SIGINT, signal_handler)

def stop_motor_high():
    motor.forward_device.on()
    motor.backward_device.on()

def flying_fish_deactivated():
    print ("Flying Fish deactivated")
    stop_motor_high()

flyingFish.when_deactivated = flying_fish_deactivated

try:
    while True:
        if buttonRight.is_pressed:
            print("Button right is pressed")
            motor.backward( 0.2 )
        if buttonLeft.is_pressed:
            print("Button left is pressed")
            motor.forward( 0.2 )
        time.sleep(0.1)

except Exception as e:
    cleanup()
