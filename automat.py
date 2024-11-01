import time
import signal
import sys
from gpiozero import DigitalOutputDevice
from gpiozero import Button
from picamera2 import Picamera2

out = DigitalOutputDevice(21)
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.set_controls({
    "ExposureTime": int(1/30 * 1_000_000),
    "AnalogueGain": 1.0,
})
picam2.start()
button = Button(26)

def cleanup():
    print("Räume auf...")
    # Hier kannst du alle Ressourcen freigeben, z.B. GPIOs, Dateien schließen usw.
    picam2.stop()
    out.off()
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup()

# Signal abfangen
signal.signal(signal.SIGINT, signal_handler)

counter = 1
try:
    while True:
        if button.is_pressed:
            print("Button is pressed")
            out.on()
            time.sleep(0.5)
            picam2.capture_file(f"images/ktl-{counter}.jpg")
            counter = counter+1
            out.off()
            while button.is_pressed:
                time.sleep(0.1)
        time.sleep(0.1)

except Exception as e:
    cleanup()
