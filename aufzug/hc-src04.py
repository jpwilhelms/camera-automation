import time
import board
import adafruit_hcsr04

# Initialisiere den HC-SR04 Sensor
#sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D27, echo_pin=board.D17)
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D17, echo_pin=board.D27)

while True:
    try:
        # Lese die Entfernung in cm
        distance = sonar.distance
        print(f"Entfernung: {distance:.2f} cm")
    except RuntimeError:
        print("Messfehler. Bitte erneut versuchen.")
    time.sleep(1)

