import board
import time
import sys
import random

from hardware import Hardware
from motorcontroller import MotorController
from pidcontroller import PIDController
from stopper import Stopper
from greifer import Greifer

class Elevator:
    def __init__(self, hw:Hardware):
        self.gyroscope_handler = hw.gyroscope_handler
        self.gripper = Greifer(hw)
        self.flatMax = 0.15
        self.flatErrorMax = 0.5
        self.shakeSeconds = 0.3 
        self.wait_for_bottom_check = 0.3

        self.controller = MotorController(hw)
        self.stopperTop = hw.stopperTop
        self.stopperDown1 = hw.stopperDown1
        self.stopperDown2 = hw.stopperDown2

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
            
            if self.stopperDown():
                time.sleep( self.wait_for_bottom_check )
                if self.gyroscope_handler.is_flat( self.flatMax ):
                    break

            print( f"not landed: {self.gyroscope_handler.get_latest_result()}" )
            start_time = time.time()

            while time.time() - start_time < self.shakeSeconds:
                self._move_single("up", self.stopperTop.isTriggered)
                time.sleep(0.1)

            self.controller.stop_motors()
            time.sleep(random.uniform(0, 4))

    def _stopperDownOrUneven(self):
        return self.stopperDown() or not self.gyroscope_handler.is_flat( self.flatErrorMax )

    def _landed(self):
        for i in range( 5 ):
            if not (self.stopperDown() and self.gyroscope_handler.is_flat( self.flatMax )):
                return False
        return True

    def shake(self):
        if not self._stopperDownOrUneven():
            print("shake is only allowed on bottom")
            return

        print( "shaking" )
        while not self._landed():
            print( f"not landed: {self.gyroscope_handler.get_latest_result()}" )
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
    if len(sys.argv) > 1:
        elevator = Elevator(Hardware())
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
                print( f"landed: {elevator.gyroscope_handler.get_latest_result()}" )
            elif action == "shake":
                elevator.shake()
            else:
                raise ValueError(f"Invalid action: {action}")
        except KeyboardInterrupt as e:
            elevator.stop()
    else:
        raise ValueError(f"Usage: {sys.argv[0]} <stop|upGrip|upRelease|down>")

