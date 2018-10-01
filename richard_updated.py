from microbit import *

def main():
    """
    LOGIC:
       Accelerate while pins either side of the line
       Decelerate when a pin sees the line until minimum speed reached
       Increase amount of turn gradually while needed and set back to zero
       as soon as line is no longer detected
    """
    display.scroll('Go', wait=False, loop=True)
    
    # TUNE THESE CONSTANTS TO GET BEST PERFORMANCE
    _ACCELERATION, _DECELERATION, _MIN_SPEED, _TURN_RATE = 0.07, 0.6, 0.3, 0.1

    _speed = _MIN_SPEED
    _current_turn = 0.0
    
    while True:
        if is_left_seeing_line():  # Slow down and turn left
            _speed -= _DECELERATION
            _speed = max(_speed, _MIN_SPEED)
            _current_turn = min(_current_turn, 0.0) - _TURN_RATE
            right_speed = _speed
            left_speed = _speed + _current_turn
        elif is_right_seeing_line():  # Slow down and turn right
            _speed -= _DECELERATION
            _speed = max(_speed, _MIN_SPEED)
            _current_turn = max(_current_turn, 0.0) + _TURN_RATE
            right_speed = _speed - _current_turn
            left_speed = _speed
        else:  # Go straight and accelerate
            _speed += _ACCELERATION
            _speed = min(_speed, 1.0)
            _current_turn = 0.0
            left_speed = _speed
            right_speed = _speed

        set_motor_speeds(left_speed, right_speed)


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
    Set the right motor speed. Speed is a float in the range [-1.0, 1.0]
    """

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
