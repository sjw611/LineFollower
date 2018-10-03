from microbit import *

def main():
    display.scroll('Smokin!', wait=False, loop=True)

    # TUNE THESE CONSTANTS TO GET BEST PERFORMANCE
    _SPEED, _TURN_RATE, _EXP = 0.8, 0.02, 1.2

    _touch_counter = 0

    while True:
        # Slow down inside wheel with exponentially greater amount
        # Or go full speed ahead
        if is_left_seeing_line():
            _touch_counter = min(_touch_counter, 0) - 1
            turn = (_EXP ** abs(_touch_counter)) * -_TURN_RATE
            right_speed = _SPEED
            left_speed = max(_SPEED + turn, -1.0)
        elif is_right_seeing_line():
            _touch_counter = max(_touch_counter, 0) + 1
            turn = (_EXP ** _touch_counter) * -_TURN_RATE
            right_speed = max(_SPEED - turn, -1.0)
            left_speed = _SPEED
        else:
            _touch_counter = 0
            left_speed = _SPEED
            right_speed = _SPEED

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
