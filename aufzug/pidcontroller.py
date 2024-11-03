class PIDController:
    def __init__(self, K_p, K_i, K_d):
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.last_error = 0
        self.integral = 0

    def compute(self, error):
        self.integral += error
        derivative = error - self.last_error
        output = self.K_p * error + self.K_i * self.integral + self.K_d * derivative
        self.last_error = error
        return output

    def reset(self):
        self.last_error = 0
        self.integral = 0
