import board
import busio
from adafruit_motor import motor
from adafruit_pca9685 import PCA9685

class Motor:
    def __init__(self, pca, forward_channel, backward_channel, id):
        self.pca = pca
        self.motor_control = motor.DCMotor(self.pca.channels[forward_channel], self.pca.channels[backward_channel])
        self.motor_control.decay_mode = motor.SLOW_DECAY
        self.speed = 0  
        self.throttle_min = 0.1
        self.throttle_max = 0.6  
        self.dir_forward = True
        self.id = id

    def set_speed(self, speed):
        """Setze die Geschwindigkeit des Motors zwischen 1 und 100."""
        if not (0 <= speed <= 100):
            raise ValueError("Speed muss zwischen 1 und 100 liegen.")
        
        self.speed = speed
        self._set_throttle()

    def set_directional_speed(self, speed, min_abs_speed: int = 20):
        """Setze die Geschwindigkeit des Motors zwischen 1 und 100."""
        if not (-100 <= speed <= 100):
            raise ValueError("Speed muss zwischen -100 und 100 liegen.")

        self.dir_forward = (speed >= 0)
        abs_speed = abs(speed)
        
        if abs_speed < min_abs_speed:
            self.stop()
        else:
            self.speed = abs_speed
            self._set_throttle()

    def forward(self):
        self.dir_forward = True
        self._set_throttle()

    def backward(self):
        self.dir_forward = False
        self._set_throttle()

    def stop(self):
        self.speed = 0
        self._set_throttle()

    def release(self):
        self.speed = None
        self._set_throttle()

    def _set_throttle(self):
        if self.speed == None:
            throttle = None
        elif self.speed == 0:
            throttle = 0
        else:
            throttle = self.throttle_min + (self.speed - 1) / 99 * (self.throttle_max - self.throttle_min)

        if (not throttle == None) and not self.dir_forward:
            throttle = -throttle

        self.motor_control.throttle = throttle

