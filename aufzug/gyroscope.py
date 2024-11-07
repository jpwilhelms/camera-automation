import time
import board
import busio
import statistics
from adafruit_mpu6050 import MPU6050

class Gyroskop:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = MPU6050(i2c)
    
    def getXY(self):
        acceleration = self.getMedian( [self.mpu.acceleration for _ in range(3)] )
        self.latestResult = acceleration[0] - 0.21, acceleration[1] + 0.10
        return self.latestResult

    def printAll(self):
        print( f"accel: {self.mpu.acceleration} m/s^2" )
        print( f"gyro: {self.mpu.gyro} °/s" )
        print( f"temp: {self.mpu.temperature} °C" )

    def isFlat(self,threshold):
        xy = self.getXY()
        result = all(abs(x) < threshold for x in xy)
        return result

    def getLatestResult(self):
        return self.latestResult

    def getMedian(self, tupel_liste):
        transponiert = zip(*tupel_liste)
        median_tupel = tuple(statistics.median(werte) for werte in transponiert)
        return median_tupel

if __name__ == "__main__":
    gyroskop = Gyroskop()
    
    while True:
        print( f"{gyroskop.getXY()}" )
        #gyroskop.printAll()
        #time.sleep(1)

