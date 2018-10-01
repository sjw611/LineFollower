from microbit import *

# If exceeds this, go straight a bit
MAX_WOBBLING = 5
STRAIGHT_LINE_SPEED = 0.7
RECOVER_WOBBLING_LINE_SPEED = 0.9
TURN_SPEED = 0.5

def main():
    display.scroll('Go', wait=False, loop=True)
    # One wobbling is from left -> right
    # or right -> left
    num_wobbling = 0
    # Last seen line on the left -1, right 1, neither 0
    last_seen = 0
    while True:
        if is_left_seeing_line():
            last_seen, num_wobbling = _handle_wobbling(
                -1, last_seen, num_wobbling)
        elif is_right_seeing_line():
            last_seen, num_wobbling = _handle_wobbling(
                1, last_seen, num_wobbling)
        else:
            set_motor_speeds(STRAIGHT_LINE_SPEED, STRAIGHT_LINE_SPEED)


def _handle_wobbling(now_seeing, last_seen, num_wobbling):
    if last_seen + now_seeing == 0:
        num_wobbling += 1
    else:
        num_wobbling = 0
    
    if num_wobbling > MAX_WOBBLING:
        num_wobbling = 0
        last_seen = 0
        set_motor_speeds(
            RECOVER_WOBBLING_LINE_SPEED, RECOVER_WOBBLING_LINE_SPEED)
    else:
        last_seen = now_seeing
        set_motor_speeds(now_seeing * TURN_SPEED, now_seeing * -TURN_SPEED)
        
    return (last_seen, num_wobbling)

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