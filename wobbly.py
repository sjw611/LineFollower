from microbit import *

# Last seen line on the left -1, right 1, neither 0
# Come on I am not bothered about enum
_last_seen = 0

# One wobbling is from left -> right
# or right -> left
_num_wobbling = 0

# If exceeds this, go straight a bit
MAX_WOBBLING = 5

_handle_wobbling(now_seeing):
    if _last_seen + now_seeing == 0:
        _num_wobbling += 1
    else:
        _num_wobbling = 0
    
    if _num_wobbling > MAX_WOBBLING:
        _num_wobbling = 0
        _last_seen = 0
        set_motor_speeds(0.1, 0.1)
    else:
        _last_seen = now_seeing
        set_motor_speeds(now_seeing * 0.2, now_seeing * -0.2)
    

def main():
    display.scroll('Go', wait=False, loop=True)
    while True:
        if is_left_seeing_line():
            _handle_
wobbling(-1)
        elif is_right_seeing_line():
            _handle_wobbling(1)
        else:
            set_motor_speeds(0.3, 0.3)


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
