import time
from hardware import Hardware

hw = Hardware()
motor1 = hw.motor1

try:
    motor1.backward()
    motor1.set_speed( 60 )
    time.sleep(1)
    motor1.stop()
except KeyboardInterrupt:
    motor1.stop()
    hw.cleanup()

hw.cleanup()
