import RPi.GPIO as GPIO
import sys
import time
import random




def main():

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	w=18
	r=22
	g=24
	b=27
	chan_list=[w,r,g,b]
	GPIO.setup(chan_list,GPIO.OUT)
	GPIO.output(chan_list,GPIO.HIGH)
	
	w1=GPIO.PWM(w,120)
	r1=GPIO.PWM(r,120)
	g1=GPIO.PWM(g,120)
	b1=GPIO.PWM(b,120)
	#white=random.randint(0,15)
	#red=random.randint(0,100)
	#green=random.randint(0,15)
	#blue=random.randint(0,15)
	white=0
	red=0
	green=0
	blue=0
	while True:
		dr=(random.uniform(0,100)-red)
		dg=(random.uniform(0,100)-green)
		db=(random.uniform(0,100)-blue)
		speed=.1
		mag=((dr**2+dg**2+db**2)**(0.5))/speed
		direction=[dr/mag,dg/mag,db/mag]
		w1.start(white)
		r1.start(red)
		g1.start(green)
		b1.start(blue)
		rnext=red+direction[0]
		gnext=green+direction[1]
		bnext=blue+direction[2]
		print red
		print green
		print blue
		print rnext
		print gnext
		print bnext
		while (0<=rnext<=100 and 0<=gnext<=100 and 0<=bnext<=100):
			red=red+direction[0]
			green=green+direction[1]
			blue=blue+direction[2]
			r1.start(red)
			g1.start(green)
			b1.start(blue)
			rnext=red+direction[0]
			gnext=green+direction[1]
			bnext=blue+direction[2]
			print red
			print green
			print blue
			print rnext
			print gnext
			print bnext
			time.sleep(.01)

try:
	main()
except KeyboardInterrupt:	
	GPIO.cleanup()
	print "Bye"
except SystemExit:
	GPIO.cleanup()
	print "Sayanora"
except:
	GPIO.cleanup()
	print "Good Bye"
