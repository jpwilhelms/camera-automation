import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Greifer:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c, address=0x40)
        self.pca.frequency = 50
        self.maxAngle = 130
        self.minAngle = 50
        
        # Servo-Objekte für Kanäle 0, 1, 2 und 3 erstellen
        self.servo_0 = servo.Servo(self.pca.channels[0])
        self.servo_1 = servo.Servo(self.pca.channels[1])
        self.servo_2 = servo.Servo(self.pca.channels[2])
        self.servo_3 = servo.Servo(self.pca.channels[3])
    
    def grip(self):
        # Alle Servos auf minimale Position setzen (0 Grad)
        self.servo_0.angle = self.maxAngle
        self.servo_1.angle = self.minAngle
        self.servo_2.angle = self.maxAngle
        self.servo_3.angle = self.minAngle
        time.sleep(1)  # Optional: Warten, bis die Bewegung abgeschlossen ist
    
    def release(self):
        # Alle Servos auf maximale Position setzen (self.maxAngle Grad)
        self.servo_0.angle = self.minAngle
        self.servo_1.angle = self.maxAngle
        self.servo_2.angle = self.minAngle
        self.servo_3.angle = self.maxAngle
        time.sleep(1)  # Optional: Warten, bis die Bewegung abgeschlossen ist
    
    def cleanup(self):
        # PCA9685 deaktivieren und aufräumen
        self.pca.deinit()

# Beispiel für die Nutzung der Greifer-Klasse
if __name__ == "__main__":
    greifer = Greifer()
    try:
        while True:
            greifer.grip()
            time.sleep(1)
            greifer.release()
            time.sleep(1)
    except KeyboardInterrupt:
        greifer.cleanup()

