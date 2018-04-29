from microbit import *

while True:
	if left_detect():
		motors(-0.2, 0.2)
	elif right_detect():
		motors(0.2, -0.2)
	else:
		motors(0.3, 0.3)

def left_detect():
    return pin1.read_analog() > 255:

def right_detect():
	return pin2.read_analog() > 255

def motors(l,r):
    left_motor(l)
    right_motor(r)

def left_motor(s):
    _motor(s,pin12,pin8,0)

def right_motor(s):
    _motor(s,pin16,pin0,1)

_p=[0,0]
def _motor(s,p0,p1,i):
    m = 0
    _p[i]+=abs(s)
    if _p[i]>1:
        m=1
        _p[i]-=1
    _pin(p0,(s>0)&m)
    _pin(p1,(s<0)&m)

def _pin(p, v):
    p.write_digital(v)

main()