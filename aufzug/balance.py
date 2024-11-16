import time
from pidcontroller import PIDController
from hardware import Hardware
from gyroscope_handler import GyroscopeHandler

hw = Hardware()
gh = GyroscopeHandler( hw.gyroscope )
gh.start()

def get_error():
    (x,y) = gh.get_average()
    return x

pid = PIDController(50,1,20)
motor = hw.motor3

while True:
    error = get_error()
    output = pid.compute( error )
    new_speed = -max(-100, min(100, output))
    print( f"Error: {error}, output: {output}, new_speed: {new_speed}")
    motor.set_directional_speed( new_speed, 20 )
    time.sleep( 0.01 )
