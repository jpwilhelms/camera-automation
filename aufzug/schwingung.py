import time
import board
import busio
import adafruit_mpu6050
import math

# Initialisierung des I2C-Bus und des MPU6050-Sensors
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Einstellungen
measurement_interval = 0.1  # Messintervall in Sekunden
stabilization_threshold = 0.05  # Schwellenwert für die Stabilisierung

def get_acceleration_magnitude():
    acc_x, acc_y, acc_z = mpu.acceleration
    magnitude = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
    return magnitude

# Funktion zur Bewertung der Schwingung
def is_stabilized(magnitudes, threshold):
    mean_magnitude = sum(magnitudes) / len(magnitudes)
    for mag in magnitudes:
        if abs(mag - mean_magnitude) > threshold:
            return False
    return True

# Liste zur Speicherung der Magnituden
magnitudes = []

print("Starte Messung...")

while True:
    magnitude = get_acceleration_magnitude()
    magnitudes.append(magnitude)
    
    if len(magnitudes) > 10:  # Behalte die letzten 10 Messungen
        magnitudes.pop(0)
    
    if len(magnitudes) == 10:
        if is_stabilized(magnitudes, stabilization_threshold):
            print("Objekt ist stabil.")
        else:
            print("Objekt schwingt noch.")
    
    time.sleep(measurement_interval)

