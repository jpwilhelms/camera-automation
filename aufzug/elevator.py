import board
import time
import sys
import random

from gyroscope import Gyroscope
from pidcontroller import PIDController
from motorcontroller import MotorController
from stopper import Stopper
from greifer import Greifer

class Elevator:
    def __init__(self):
        self.gyroscope = Gyroscope()
        self.gripper = Greifer()
        kp = 30
        ki = 2
        kd = 1 
        self.flatMax = 0.25
        self.flatErrorMax = 0.4
        self.shakeSeconds = 0.8 

        self.pid_x = PIDController(K_p=kp, K_i=ki, K_d=kd)
        self.pid_y = PIDController(K_p=kp, K_i=ki, K_d=kd)

        self.controller = MotorController(self.gyroscope, self.pid_x, self.pid_y)
        self.stopperTop = Stopper(board.D5)
        self.stopperDown1 = Stopper(board.D6)
        self.stopperDown2 = Stopper(board.D10)

    def stop(self):
        self.controller.stop_motors()
        time.sleep(0.5)
        self.controller.release_motors()
        print("stopped")

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
            self._resetPids()
            start_time = time.time()

            while time.time() - start_time < self.shakeSeconds:
                self._move_single("up", self.stopperTop.isTriggered)
                time.sleep(0.1)

            self.controller.stop_motors()
            time.sleep(random.uniform(0, 4))

    def _resetPids(self):
        self.pid_x.reset()
        self.pid_y.reset()

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
#            time.sleep(0.001)

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
        try:
            if action == "stop":
                elevator.stop()
            elif action == "upGrip":
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
        except KeyboardInterrupt as e:
            elevator.stop()
    else:
        raise ValueError(f"Usage: {sys.argv[0]} <stop|upGrip|upRelease|down>")

