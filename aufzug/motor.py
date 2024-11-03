import board
import digitalio
import pwmio
import time

class Motor:
    def __init__(self, pwm_pin, dir_pin1, dir_pin2, frequency=1000):
        self.enb = pwmio.PWMOut(pwm_pin, frequency=frequency, duty_cycle=0)
        self.in1 = digitalio.DigitalInOut(dir_pin1)
        self.in1.direction = digitalio.Direction.OUTPUT
        self.in2 = digitalio.DigitalInOut(dir_pin2)
        self.in2.direction = digitalio.Direction.OUTPUT
        
        # Initially set direction to forward
        self.stop()

    def stop(self):
        self.in1.value = True
        self.in2.value = True
        self.set_speed( 100 )

    def forward(self):
        self.in1.value = True
        self.in2.value = False

    def backward(self):
        self.in1.value = False
        self.in2.value = True

    def set_speed(self, speed):
        if speed < 0:
            speed = 0
        if speed > 100:
            speed = 100
        self.enb.duty_cycle = int(speed * 65535) // 100  # Scale speed to PWM duty cycle range (0-65535)

# Beispiel-Nutzung:
if __name__ == "__main__":
    motor = Motor(board.D16, board.D20, board.D21)

    while True:
        motor.set_speed(60)  # Set speed to 60%
        time.sleep(1)
        motor.set_speed(40)  # Set speed to 40%
        time.sleep(1)
        motor.backward()
        motor.set_speed(60)  # Set speed to 60%
        time.sleep(1)
        motor.set_speed(40)  # Set speed to 40%
        time.sleep(1)
        motor.forward()

