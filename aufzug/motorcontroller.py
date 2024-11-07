import board
import busio

from adafruit_pca9685 import PCA9685
from motor import Motor

class MotorController:
    def __init__(self, gyroscope, pid_x, pid_y):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c, address=0x41)
        self.pca.frequency = 1500
        self.motor1 = Motor( self.pca, 0, 1 )
        self.motor2 = Motor( self.pca, 2, 3 )
        self.motor3 = Motor( self.pca, 8, 9 )
        self.gyroscope = gyroscope
        self.pid_x = pid_x
        self.pid_y = pid_y
        self.speed_up = 60
        self.speed_down = 40 

    def __adjust_motors(self, direction):
        x_angle, y_angle = self.gyroscope.getXY()
        print( f"x: {x_angle}, y: {y_angle}" )
        
        # Berechne die Ausgangssignale der PID-Regler für x und y
        output_x = self.pid_x.compute(x_angle)
        output_y = self.pid_y.compute(y_angle)
        
        # Beispiel: Anpassung der Motorgeschwindigkeiten basierend auf den PID-Ausgangswerten
        if direction == "up":
            speed1 = self.speed_up + output_x + output_y
            speed2 = self.speed_up + output_x - output_y
            speed3 = self.speed_up - output_x
        elif direction == "down":
            speed1 = self.speed_down - output_x - output_y
            speed2 = self.speed_down - output_x + output_y
            speed3 = self.speed_down + output_x
        else:
            raise ValueError( "direction has to be up or down" )

        speed1 = self.__adjust_speed( speed1 )
        speed2 = self.__adjust_speed( speed2 )
        speed3 = self.__adjust_speed( speed3 )

        self.motor1.set_speed( speed1 )
        self.motor2.set_speed( speed2 )
        self.motor3.set_speed( speed3 )
        # print( f'{speed1}, {speed2}, {speed3}' )

    def __adjust_speed(self, speed):
        if speed < 0:
            return 0

        if speed > 100:
            return 100

        return speed

    def up(self):
        for motor in (self.motor1, self.motor2, self.motor3):
            motor.forward()
        self.__adjust_motors( "up" )

    def down(self):
        for motor in (self.motor1, self.motor2, self.motor3):
            motor.backward()
        self.__adjust_motors( "down" )

    def release_motors(self):
        self.motor1.release()
        self.motor2.release()
        self.motor3.release()
        self.pid_x.reset()
        self.pid_y.reset()

    def stop_motors(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.pid_x.reset()
        self.pid_y.reset()
