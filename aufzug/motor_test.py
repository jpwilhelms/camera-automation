import time
from hardware import Hardware

hw = Hardware()

hw.motor1.backward()
hw.motor2.backward()
hw.motor1.set_speed( 10 )
hw.motor2.set_speed( 10 )
time.sleep(1)
