import time
import board
import busio
from adafruit_pca9685 import PCA9685
from motor import Motor

# I2C-Bus initialisieren
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685-Objekt erstellen
pca = PCA9685(i2c)
pca.frequency = 1200

motor1 = Motor(pca, 8, 9)

try:
    for speed in range( 5, 101, 5 ):
        print( f"speed: {speed}" )
        motor1.set_speed( speed )
        time.sleep(1)
    motor1.stop()
except KeyboardInterrupt:
    motor1.stop()
    pca.deinit()

time.sleep(1)
pca.deinit()
