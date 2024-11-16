import time
from hardware import Hardware
from gyroscope_handler import GyroscopeHandler

hw = Hardware()
gh = GyroscopeHandler(hw.gyroscope)
gh.start()

# up = positive, down = negative
speed = 40
trigger_angle = 1
hw.motor1.forward()
hw.motor2.forward()
hw.motor3.forward()

input("Bereit für Motor1?")
time.sleep(1)
hw.motor1.set_speed(speed)

while True:
    error = gh.get_average()
    if error[0] < -trigger_angle:
        hw.motor1.stop()
        break
    time.sleep(0.01)

input("Bereit für Motor3?")
time.sleep(1)
hw.motor3.set_speed(speed)

while True:
    error = gh.get_average()
    if error[0] > trigger_angle:
        hw.motor3.stop()
        break
    time.sleep(0.01)

input("Bereit für Motor2?")
time.sleep(1)
hw.motor2.set_speed(speed)

while True:
    error = gh.get_average()
    if error[0] < -trigger_angle:
        hw.motor2.stop()
        break
    time.sleep(0.01)

#-1
#+1
#+1