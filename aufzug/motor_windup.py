import time
from hardware import Hardware
from gyroscope_handler import GyroscopeHandler

hw = Hardware()
gh = hw.gyroscope_handler

# up = positive, down = negative
speed = 10
trigger_angle = 1
trigger_angle_even = 0.2
hw.motor1.forward()
hw.motor2.forward()
hw.motor3.forward()

def windup_motor( motor, number ):
    input(f"Bereit für Motor{number}?")
    time.sleep(1)
    motor.set_speed(speed)
    
    while gh.is_flat(trigger_angle):
        time.sleep(0.01)

    motor.stop()
    motor.backward()
    motor.set_speed(speed)

    while not gh.is_flat(trigger_angle_even):
        time.sleep(0.01)

    motor.stop()

windup_motor( hw.motor1, 1 )
windup_motor( hw.motor2, 2 )
windup_motor( hw.motor3, 3 )
