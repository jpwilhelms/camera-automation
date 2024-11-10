import time
import board
import busio
from adafruit_pca9685 import PCA9685
from motor import Motor

# I2C-Bus initialisieren
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685-Objekt erstellen
pca = PCA9685(i2c, address=0x41)
pca.frequency = 1200

motor1 = Motor(pca, 8, 9, "test")

try:
    motor1.backward()
    motor1.set_speed( 60 )
    time.sleep(2)
    motor1.stop()
except KeyboardInterrupt:
    motor1.stop()
    pca.deinit()

pca.deinit()
