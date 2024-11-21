import time
from calculate_motor_speeds_with_target_velocity import calculate_motor_speeds_with_target_velocity
from greifer import Greifer
from pidcontroller import PIDController
from hardware import Hardware
from gyroscope_handler import GyroscopeHandler

hw = Hardware()
gh = GyroscopeHandler(hw.gyroscope)
gh.start()
greifer = Greifer(hw)

# up = positive, down = negative
target_speed = -10
has_weight = True
even_max = 1

if has_weight:
    Kp = 30
else:
    Kp = 5

max_speed = 100

if target_speed >= 30:
    greifer.grip()
elif target_speed > 0:
    greifer.release()

def _directional_stopper_reached():
    if target_speed > 0:
        return hw.stopperTop.isTriggered()
    else:
        return hw.stopperDown1.isTriggered() or hw.stopperDown2.isTriggered()
    
def _is_very_uneven( error ):
    return abs(error[0]) > even_max or abs(error[1]) > even_max

while not _directional_stopper_reached():
    error = gh.get_average()

    if _is_very_uneven( error ):
        print( "very uneven, terminating!" )
        break

    new_speed_1, new_speed_2, new_speed_3 = calculate_motor_speeds_with_target_velocity(error[0], error[1], target_speed)
    print(
        f"Error: {error}, new_speed: 1={new_speed_1}, 2={new_speed_2}, 3={new_speed_3}"
    )
    hw.motor1.set_directional_speed(new_speed_1)
    hw.motor2.set_directional_speed(new_speed_2)
    hw.motor3.set_directional_speed(new_speed_3)
    time.sleep(0.01)
