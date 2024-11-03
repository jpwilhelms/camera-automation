import time
import board
import busio
from adafruit_mpu6050 import MPU6050

class Gyroskop:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.mpu = MPU6050(i2c)
    
    def getXY(self):
        acceleration = self.mpu.acceleration
        self.latestResult = acceleration[0] + 0.3, acceleration[1] + 0.2
        return self.latestResult

    def isFlat(self,threshold):
        xy = self.getXY()
        result = all(abs(x) < threshold for x in xy)
        return result

    def getLatestResult(self):
        return self.latestResult

if __name__ == "__main__":
    gyroskop = Gyroskop()
    
    while True:
        # Daten abrufen
        x_accel, y_accel = gyroskop.getXY()
        
        # Daten ausgeben
        print(f"X-Beschleunigung: {x_accel:.2f} m/s^2")
        print(f"Y-Beschleunigung: {y_accel:.2f} m/s^2")
        gyroskop.isFlat( 1.5 )
        print("")
        
        # Eine Sekunde warten
        time.sleep(1)

