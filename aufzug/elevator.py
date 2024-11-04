import board
import time
import sys
import random
import busio

from gyroscope import Gyroskop
from pidcontroller import PIDController
from motorcontroller import MotorController
from motor import Motor
from stopper import Stopper
from greifer import Greifer
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

class Elevator:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 1200

        self.motor1 = Motor( self.pca, 6, 7 )
        self.motor2 = Motor( self.pca, 4, 5 )
        self.motor3 = Motor( self.pca, 8, 9 )
        self.gyroscope = Gyroskop()
        self.gripper = Greifer()
        kp = 30
        ki = 1 
        kd = 3 
        self.flatMax = 0.25
        self.flatErrorMax = 1
        self.shakeSeconds = 1.8

        self.pid_x = PIDController(K_p=kp, K_i=ki, K_d=kd)
        self.pid_y = PIDController(K_p=kp, K_i=ki, K_d=kd)

        self.controller = MotorController(self.motor1, self.motor2, self.motor3, self.gyroscope, self.pid_x, self.pid_y)
        self.stopperTop = Stopper(board.D5)
        self.stopperDown1 = Stopper(board.D6)
        self.stopperDown2 = Stopper(board.D10)

    def upGrip(self):
        if self.stopperTop.isTriggered():
            print("already on top")
            return

        if not self.stopperDown():
            print("grip change is only allowed on bottom")
            return

        self.gripper.grip()
        self._move("up", self.stopperTop.isTriggered)

    def stopperDown(self):
        return self.stopperDown1.isTriggered() and self.stopperDown2.isTriggered()

    def upRelease(self):
        if self.stopperTop.isTriggered():
            print("already on top")
            return

        if not self.stopperDown():
            print("grip change is only allowed on bottom")
            return

        self.gripper.release()
        self._move("up", self.stopperTop.isTriggered)

    def up(self):
        if self.stopperTop.isTriggered():
            print("already on top")
            return

        self._move("up", self.stopperTop.isTriggered)

    def down(self):
        if self.stopperDown():
            print("already on bottom")
            return

        while True:
            self._move("down", self._stopperDownOrUneven)
            #self._move("down", self.stopperDown)
            
            if self.stopperDown():
                time.sleep( 0.5 )
                if self.gyroscope.isFlat( self.flatMax ):
                    break

            print( f"not landed: {self.gyroscope.getLatestResult()}" )
            start_time = time.time()

            while time.time() - start_time < self.shakeSeconds:
                self._move_single("up", self.stopperTop.isTriggered)
                time.sleep(0.1)

            self.controller.stop_motors()
            time.sleep(random.uniform(0, 4))

    def _stopperDownOrUneven(self):
        return self.stopperDown() or not self.gyroscope.isFlat( self.flatErrorMax )

    def _landed(self):
        for i in range( 5 ):
            if not (self.stopperDown() and self.gyroscope.isFlat( self.flatMax )):
                return False
        return True

    def shake(self):
        if not self._stopperDownOrUneven():
            print("shake is only allowed on bottom")
            return

        while not self._landed():
            print( f"not landed: {self.gyroscope.getLatestResult()}" )
            start_time = time.time()

            while time.time() - start_time < self.shakeSeconds:
                self._move_single("up", self.stopperTop.isTriggered)
                time.sleep(0.1)

            self.controller.stop_motors()
            time.sleep(random.uniform(0, 4))
            self.down()
            time.sleep(0.5)

    def _move(self, direction, stopperCheck):
        while True:
            if not self._move_single(direction, stopperCheck):
                break
            time.sleep(0.1)

    def _move_single(self, direction, stopperCheck):
        if stopperCheck():
            self.controller.stop_motors()
            return False

        if direction == "up":
            self.controller.up()
        elif direction == "down":
            self.controller.down()

        return True

if __name__ == "__main__":
    elevator = Elevator()

    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "upGrip":
            elevator.upGrip()
        elif action == "upRelease":
            elevator.upRelease()
        elif action == "up":
            elevator.up()
        elif action == "down":
            elevator.down()
            print( f"landed: {elevator.gyroscope.getLatestResult()}" )
        elif action == "shake":
            elevator.shake()
        else:
            raise ValueError(f"Invalid action: {action}")
    else:
        raise ValueError(f"Usage: {sys.argv[0]} <upGrip|upRelease|down>")

