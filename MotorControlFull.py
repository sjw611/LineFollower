from microbit import *

def main():
	pass


def left_seeing_line():
	"""
	Returns True iff the left sensor is detecting the black line.
	"""
    return pin1.read_analog() > 255:


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
    _motor(speed, pin12, pin8, pwm_index=0)


def right_motor(speed):
	"""
	Set the right motor speed. Speed is a float in the range [-1.0, 1.0]"""
    _motor(speed, pin16, pin0, pwm_index=1)

	
_pwm_counters = [0, 0] 
# These counters are the globals used to keep track 
# of the pwm (pulse width modulation) counters used to set motor
# speed to non binary values.

def _set_motor(speed, forward_pin, backward_pin, pwm_index):
    is_going_forward = speed > 0
	is_going_backwards = speed < 0
	is_motor_on = False
    _pwm_counters[pwm_index]+=abs(s)
    if _pwm_counters[pwm_index] > 1:
        is_motor_on = True
        _pwm_counters[pwm_index] -= 1
    _set_pin(forward_pin, is_going_forward & is_motor_on)
    _set_pin(backward_pin, is_going_backwards & is_motor_on)

        
def _set_pin(pin, value):
    pin.write_digital(value)


main()