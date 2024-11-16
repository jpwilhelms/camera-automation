import time
from hardware import Hardware

class Greifer:
    def __init__(self, hw: Hardware):
        self.maxAngle = 130
        self.minAngle = 50
        
        # Servo-Objekte für Kanäle 0, 1, 2 und 3 erstellen
        self.servo_0 = hw.servo_0
        self.servo_1 = hw.servo_1
        self.servo_2 = hw.servo_2
        self.servo_3 = hw.servo_3
    
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
    
# Beispiel für die Nutzung der Greifer-Klasse
if __name__ == "__main__":
    hw = Hardware()
    greifer = Greifer( hw )
    try:
        while True:
            greifer.grip()
            time.sleep(1)
            greifer.release()
            time.sleep(1)
    except KeyboardInterrupt:
        hw.cleanup()

