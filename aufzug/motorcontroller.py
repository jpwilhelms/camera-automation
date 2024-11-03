class MotorController:
    def __init__(self, motor1, motor2, motor3, gyroscope, pid_x, pid_y):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3
        self.gyroscope = gyroscope
        self.pid_x = pid_x
        self.pid_y = pid_y
        self.speed = 60

    def __adjust_motors(self, direction):
        x_angle, y_angle = self.gyroscope.getXY()
        
        # Berechne die Ausgangssignale der PID-Regler für x und y
        output_x = self.pid_x.compute(x_angle)
        output_y = self.pid_y.compute(y_angle)
        
        # Beispiel: Anpassung der Motorgeschwindigkeiten basierend auf den PID-Ausgangswerten
        if direction == "up":
            speed1 = self.speed + output_x + output_y
            speed2 = self.speed + output_x - output_y
            speed3 = self.speed - output_x
        elif direction == "down":
            speed1 = self.speed - output_x - output_y
            speed2 = self.speed - output_x + output_y
            speed3 = self.speed + output_x
        else:
            raise ValueError( "direction has to be up or down" )

        self.motor1.set_speed( speed1 )
        self.motor2.set_speed( speed2 )
        self.motor3.set_speed( speed3 )
        # print( f'{speed1}, {speed2}, {speed3}' )

    def up(self):
        for motor in (self.motor1, self.motor2, self.motor3):
            motor.forward()
        self.__adjust_motors( "up" )

    def down(self):
        for motor in (self.motor1, self.motor2, self.motor3):
            motor.backward()
        self.__adjust_motors( "down" )

    def stop_motors(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.pid_x.reset()
        self.pid_y.reset()
