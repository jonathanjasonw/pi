import RPi.GPIO as GPIO
import sys
import time
import random
import socket
import threading
import multiprocessing



def cube(red,green,blue):
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	r=22
	g=24
	b=27
	chan_list=[r,g,b]
	GPIO.setup(chan_list,GPIO.OUT)
	GPIO.output(chan_list,GPIO.HIGH)
	
	r1=GPIO.PWM(r,120)
	g1=GPIO.PWM(g,120)
	b1=GPIO.PWM(b,120)
	#r1.start(0)
	#g1.start(0)
	#b1.start(0)
	while True:
		dr=(random.uniform(0,100)-red)
		dg=(random.uniform(0,100)-green)
		db=(random.uniform(0,100)-blue)
		speed=0.8
		mag=((dr**2+dg**2+db**2)**(0.5))/speed
		direction=[dr/mag,dg/mag,db/mag]
		r1.ChangeDutyCycle(red)
		g1.ChangeDutyCycle(green)
		b1.ChangeDutyCycle(blue)
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
			r1.ChangeDutyCycle(red)
			g1.ChangeDutyCycle(green)
			b1.ChangeDutyCycle(blue)
			rnext=red+direction[0]
			gnext=green+direction[1]
			bnext=blue+direction[2]
			print red
			print green
			print blue
			print rnext
			print gnext
			print bnext
			time.sleep(.02)

def party(red,green,blue,rvel,gvel,bvel,r1,g1,b1):
	rvel=0.5
	gvel=0.5
	bvel=0.5
	while True:
	
			
		if 0 < round(red) and round(red) < 100.0:
			red+=rvel
	
		elif round(red) >= 100.0:
			rvel=rvel*-1
			red=rvel+100
		else:
			rvel=100/float(random.randint(10,100))
			red+=rvel
		
		if 0 < round(green) and round(green) < 100.0:
			green+=gvel

		elif round(green) >= 100.0:
			gvel=gvel*-1
			green=gvel+100
		else:
			gvel=100/float(random.randint(10,100))
			green+=gvel
		
		if 0 < round(blue) and round(blue) < 100.0:
			blue+=bvel

		elif round(blue) >= 100.0:
			bvel=bvel*-1
			blue=bvel+100
		else:
			bvel=100/float(random.randint(10,100))
			blue+=bvel
	
		print red
		print green
		print blue	
		r1.start(abs(red))
		g1.start(abs(green))
		b1.start(abs(blue))

		time.sleep(.1)


def onecolor(r1,g1,b1,red,green,blue):
	
#	while True:
		r1.start(red)
		g1.start(green)
		b1.start(blue)
		
def clear(r1,g1,b1):

	r1.start(0)
	g1.start(0)
	b1.start(0)



def christmas(r1,g1,b1):
	red=100
	green=0
	while True:
		red=100-red
		green=100-green
		r1.start(red)
		g1.start(green)
		time.sleep(1)
			
def main():



	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	r=22
	g=24
	b=27
	chan_list=[r,g,b]
	GPIO.setup(chan_list,GPIO.OUT)
	GPIO.output(chan_list,GPIO.HIGH)
	
	r1=GPIO.PWM(r,120)
	g1=GPIO.PWM(g,120)
	b1=GPIO.PWM(b,120)
	r1.start(0)
	g1.start(0)
	b1.start(0)
	#red=random.randint(0,100)
	#green=random.randint(0,15)
	#blue=random.randint(0,15)
	red=0
	green=0
	blue=0
	#cube(red,green,blue,r1,g1,b1)
	wvel = 0
	rvel = 0
	gvel = 0
	bvel = 0
	#party(red,green,blue,rvel,bvel,gvel,r1,g1,b1)
	#onecolor(r1,g1,b1)
	print(r1)
	mysocket = socket.socket()
	host = socket.gethostbyname(socket.getfqdn()) #ip of raspberry pi
	port = 9876


	if host == "127.0.1.1":
		import commands
		host = commands.getoutput("hostname -I")
	print "host = " + host

	#Prevent socket.error: [Errno 98] Address is already in use
	mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	mysocket.bind((host, port))

	mysocket.listen(5)

	(c, addr) = mysocket.accept()
	
	

	while True:
	
		data = c.recv(1024)
		data = data.replace("\r\n", '') #remove new line character
		data2 = data.split(",")
		print data2
		print data2[0]
#		print double(data2[1])
#		print double(data2[3])
		cflag=0
		pflag=0
#		if data != [''] and cflag == 1:
#			if cubethread.isalive():
#				cubethread.terminate()
#		if data != [''] and pflag == 1:
#			if partythread.isalive():
#				partythread.terminate()			
		if data2[0] == "Cube":
			cflag=1
			GPIO.cleanup()
			cubethread = multiprocessing.Process(target=cube,args=[red,green,blue])
			cubethread.daemon = False
			cubethread.start()
			#cube(red,green,blue)
		elif data2[0] == "one":
			#onecolorthread = multiprocessing.Process(target=onecolor,args=[r1,g1,b1,float(data2[1]),float(data2[2]),float(data2[3])])
			onecolor(r1,g1,b1,float(data2[1]),float(data2[2]),float(data2[3]))
		elif data2[0] == "Party":
			pflag=1
			partythread = multiprocessing.Process(target=party,args=[red,green,blue,rvel,gvel,bvel,r1,g1,b1])
			partythread.daemon = True
			partythread.start()
			#party(red,green,blue,rvel,gvel,bvel,r1,g1,b1)
		elif data2[0] == "Christmas":
			christmas(r1,g1,b1)
		elif data2[0] == "Clear":
			clear(r1,g1,b1) 
		elif data2[0] == "Quit": 
			break



		c.send("Hello from Raspberry Pi!\nYou sent: " + data + "\nfrom: " + addr[0] + "\n")


	c.send("Server stopped\n")
	print "Server stopped"
	c.close()

	
try:
	main()
except KeyboardInterrupt:
	GPIO.cleanup()
	print "buh-bye!"
except:
	GPIO.cleanup()
	print "Bye"
