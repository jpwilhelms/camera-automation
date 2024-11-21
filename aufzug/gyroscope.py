import time
import board
import busio
import statistics
from adafruit_mpu6050 import MPU6050

class Gyroscope:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = MPU6050(i2c)
    
    def getXY(self):
        acceleration = self.mpu.acceleration
        self.latestResult = acceleration[0] - 0.21, acceleration[1] + 0.10
        return self.latestResult

    def printAll(self):
        print( f"accel: {self.mpu.acceleration} m/s^2" )
        print( f"gyro: {self.mpu.gyro} °/s" )
        print( f"temp: {self.mpu.temperature} °C" )

if __name__ == "__main__":
    gyroskop = Gyroscope()
    
    while True:
        print( f"{gyroskop.getXY()}" )
        #gyroskop.printAll()
        #time.sleep(1)

