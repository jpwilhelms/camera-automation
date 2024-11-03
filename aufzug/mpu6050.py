import time
import board
import busio
from adafruit_mpu6050 import MPU6050

# I2C-Bus initialisieren
i2c = busio.I2C(board.SCL, board.SDA)

# MPU6050-Sensor initialisieren
mpu = MPU6050(i2c)

while True:
    # Sensordaten auslesen
    acceleration = mpu.acceleration
    gyro = mpu.gyro
    temperature = mpu.temperature

    # Sensordaten ausgeben
    print(f"Beschleunigung: X={acceleration[0]:.2f}, Y={acceleration[1]:.2f}, Z={acceleration[2]:.2f} m/s^2")
    print(f"Gyroskop: X={gyro[0]:.2f}, Y={gyro[1]:.2f}, Z={gyro[2]:.2f} rad/s")
    print(f"Temperatur: {temperature:.2f} °C")
    print("")

    # Eine Sekunde warten
    time.sleep(1)

