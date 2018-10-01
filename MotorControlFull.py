from microbit import *


def main():
    display.scroll('Go', wait=False, loop=True)
    while True:
        if is_left_seeing_line():
            set_motor_speeds(-0.5, 0.5)
        elif is_right_seeing_line():
            set_motor_speeds(0.5, -0.5)
        else:
            set_motor_speeds(0.8, 0.8)


def is_left_seeing_line():
    """
    Returns True iff the left sensor is detecting the black line.
    """
    return pin1.read_analog() > 255


def is_right_seeing_line():
    """
    Returns True iff the right sensor is detecting the black line.
    """
    return pin2.read_analog() > 255


def set_motor_speeds(left_speed, right_speed):
    """
    Set both motor speeds. Speeds are floats in the range [-1.0, 1.0]
    """
    left_motor(left_speed)
    right_motor(right_speed)


def left_motor(speed):
    """
    Set left motor speed. Speed is a float in the range [-1.0, 1.0]
    """
    _set_motor(speed, pin12, pin8, pwm_index=0)


def right_motor(speed):
    """
    Set the right motor speed. Speed is a float in the range [-1.0, 1.0]"""
    _set_motor(speed, pin16, pin0, pwm_index=1)



# These counters are the globals used to keep track
# of the pwm (pulse width modulation) signals used to set motor
# speed to non binary values.
_pwm_counters = [0, 0]


def _set_motor(speed, forward_pin, backward_pin, pwm_index):
    #  Increments the counter by the speed, if the counter goes over 1
    #  then turn the motor on and reset the counter. 
    is_going_forward = speed > 0
    is_going_backwards = speed < 0
    is_motor_on = False
    _pwm_counters[pwm_index] += abs(speed)
    if _pwm_counters[pwm_index] > 1:
        is_motor_on = True
        _pwm_counters[pwm_index] -= 1
    _set_pin(forward_pin, is_going_forward & is_motor_on)
    _set_pin(backward_pin, is_going_backwards & is_motor_on)


def _set_pin(pin, value):
    pin.write_digital(value)


main()