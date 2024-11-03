import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# I2C-Bus initialisieren
i2c = busio.I2C(board.SCL, board.SDA)

# PCA9685-Objekt erstellen
pca = PCA9685(i2c)
pca.frequency = 50

# Servo-Objekt für Kanal 0 erstellen
servo_1 = servo.Servo(pca.channels[0])

# Servo bewegen
def move_servo(angle):
    servo_1.angle = angle
    time.sleep(1)

# Beispiel: Servo zu verschiedenen Winkeln bewegen
try:
    while True:
        for angle in range(0, 180, 10):
            move_servo(angle)
        for angle in range(180, 0, -10):
            move_servo(angle)
except KeyboardInterrupt:
    # PCA9685 deaktivieren und aufräumen
    pca.deinit()

