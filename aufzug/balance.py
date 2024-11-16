import time
from pidcontroller import PIDController
from hardware import Hardware
from gyroscope_handler import GyroscopeHandler

hw = Hardware()
gh = GyroscopeHandler(hw.gyroscope)
gh.start()

# up = positive, down = negative
offset_speed = -20
min_speed = 0
k_p = 40
k_i = 0
k_d = 10
pid_x = PIDController(k_p, k_i, k_d)
pid_y = PIDController(k_p, k_i, k_d)


def _fit_to_range(speed):
    return max(-100, min(100, speed))


while True:
    error = gh.get_average()
    output_x = pid_x.compute(error[0])
    output_y = pid_y.compute(error[1]) / 2
    new_speed_1 = _fit_to_range(output_y+output_x+offset_speed)
    new_speed_2 = _fit_to_range(-output_y+output_x+offset_speed)
    new_speed_3 = _fit_to_range(-output_x+offset_speed)
    print(
        f"Error: {error}, output: {output_x},{output_y}, new_speed: 1={new_speed_1}, 2={new_speed_2}, 3={new_speed_3}"
    )
    hw.motor1.set_directional_speed(new_speed_1, min_speed)
    hw.motor2.set_directional_speed(new_speed_2, min_speed)
    hw.motor3.set_directional_speed(new_speed_3, min_speed)
    time.sleep(0.01)
