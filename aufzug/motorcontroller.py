from calculate_motor_speeds_with_target_velocity import calculate_motor_speeds_with_target_velocity
from gyroscope_handler import GyroscopeHandler
from hardware import Hardware
from motor import Motor

class MotorController:
    def __init__(self, hw: Hardware):
        self.motor1 = hw.motor1
        self.motor2 = hw.motor2
        self.motor3 = hw.motor3
        self.gyroscope_handler = hw.gyroscope_handler
        self.speed_up = 80
        self.speed_down = 60 

    def __adjust_motors(self, direction):
        x_angle, y_angle = self.gyroscope_handler.get_average()
        print( f"x-angle: {x_angle}, y-angle: {y_angle}, going {direction}" )
        
        if direction == "up":
            speed = self.speed_up
        elif direction == "down":
            speed = -self.speed_down
        else:
            raise ValueError( "direction has to be up or down" )

        speed1, speed2, speed3 = calculate_motor_speeds_with_target_velocity( x_angle, y_angle, speed )
        self.motor1.set_directional_speed( speed1 )
        self.motor2.set_directional_speed( speed2 )
        self.motor3.set_directional_speed( speed3 )
        # print( f'{speed1}, {speed2}, {speed3}' )

    def up(self):
        for motor in (self.motor1, self.motor2, self.motor3):
            motor.forward()
        self.__adjust_motors( "up" )

    def down(self):
        for motor in (self.motor1, self.motor2, self.motor3):
            motor.backward()
        self.__adjust_motors( "down" )

    def release_motors(self):
        self.motor1.release()
        self.motor2.release()
        self.motor3.release()

    def stop_motors(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
