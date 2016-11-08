## This script just pumps random current and voltage data 
## onto a redis published 'adc'
## used for testing socket.io connection

import redis
import random
import time

r = redis.Redis()

current = 1
voltage = 1

def get_current():
	global current
	current += (random.random()  - 0.5 ) * 0.5 
	return round(current,2)

def get_voltage():
	global voltage
	voltage += (random.random()  - 0.5 ) * 0.5 
	return round(voltage,2)


while True:
	v = get_voltage()
	c = get_current()
	msg = v
	msgc = c
	r.publish('adc', msg)
	r.publish('adc', msgc)
	print msg
	print msgc
	time.sleep(0.5)