import time
import signal
import sys
from gpiozero import Button

buttonRight = Button(26)
buttonLeft = Button(12)


def cleanup():
    print("Räume auf...")
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        if buttonRight.is_pressed:
            print("Button right is pressed")
        if buttonLeft.is_pressed:
            print("Button left is pressed")
        time.sleep(0.1)

except Exception as e:
    cleanup()
