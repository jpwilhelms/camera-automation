def calculate_motor_speeds_with_target_velocity(delta_x, delta_y, target_velocity):
    max_speed = 100
    Kp = 30
    
    # Berechne die Geschwindigkeit für jeden Motor in Bezug auf den Fehler
    motor_1_speed = delta_y * Kp/2   # Motor 1 erhöht Y, verringert X
    motor_2_speed = -delta_y * Kp/2  # Motor 2 verringert Y, verringert X
    motor_3_speed = -delta_x * Kp  # Motor 3 soll X erhöhen, wenn delta_x negativ ist

    # Kombiniere die Geschwindigkeit des Motors mit der Zielgeschwindigkeit
    # Die Zielgeschwindigkeit wird auf den Fehler angewendet
    motor_1_speed += target_velocity
    motor_2_speed += target_velocity
    motor_3_speed += target_velocity

    # Begrenze die Geschwindigkeit der Motoren auf den maximalen Wert
    motor_1_speed = min(max(motor_1_speed, -max_speed), max_speed)
    motor_2_speed = min(max(motor_2_speed, -max_speed), max_speed)
    motor_3_speed = min(max(motor_3_speed, -max_speed), max_speed)

    return motor_1_speed, motor_2_speed, motor_3_speed