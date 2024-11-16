import atexit
import board
import busio

from adafruit_pca9685 import PCA9685
from stopper import Stopper
from motor import Motor
from gyroscope import Gyroscope
from adafruit_motor import servo

class Hardware:
    def __init__(self):
        atexit.register(self.cleanup)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca41 = PCA9685(i2c, address=0x41)
        self.pca41.frequency = 1500
        self.motor1 = Motor( self.pca41, 0, 1, "1" )
        self.motor2 = Motor( self.pca41, 2, 3, "2" )
        self.motor3 = Motor( self.pca41, 8, 9, "3" )
        self.gyroscope = Gyroscope()

        self.pca40 = PCA9685(i2c, address=0x40)
        self.pca40.frequency = 50
        self.maxAngle = 130
        self.minAngle = 50
        
        # Servo-Objekte für Kanäle 0, 1, 2 und 3 erstellen
        self.servo_0 = servo.Servo(self.pca40.channels[0])
        self.servo_1 = servo.Servo(self.pca40.channels[1])
        self.servo_2 = servo.Servo(self.pca40.channels[2])
        self.servo_3 = servo.Servo(self.pca40.channels[3])

        self.stopperDown1 = Stopper(board.D5)
        self.stopperDown2 = Stopper(board.D6)
        self.stopperTop = Stopper(board.D10)


    def cleanup(self):
        print( "cleaning up hardware..." )
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.pca40.deinit()
        self.pca41.deinit()

if __name__ == "__main__":
    hw = Hardware()
    print( f"{hw.gyroscope.getXY()}" )

