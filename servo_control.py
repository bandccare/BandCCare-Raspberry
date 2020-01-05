import RPi.GPIO as GPIO
import time
import requests
import json

pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin,50)
p.start(0)

left_angle = 10
left_center_angle = 8.75
center_angle = 7.5
right_center_angle = 6.25
right_angle = 5

def doAngle(angle):
	p.ChangeDutyCycle(angle)
	time.sleep(0.5)

f = open("/home/pi/rsl.txt","r")
data = f.read()

if(float(data) > 125):
	doAngle(right_angle)

elif(float(data) > 95 and float(data) <= 125):
	doAngle(right_center_angle)

if(float(data) >= 65 and float(data) <= 95):
	doAngle(center_angle)

elif(float(data) >= 30 and float(data) < 65):
	doAngle(left_center_angle)

elif(float(data) < 30):
	doAngle(left_angle)


print(data)
f.close()

time.sleep(2)

while True:

	url_servo = "http://192.168.0.3:5000/post"
	response_u = requests.get(url=url_servo)
	j_servo = response_u.json()

	rsl = j_servo["rsl"]
	print(rsl)

	if(rsl == "left"):
		doAngle(left_angle)

	elif(rsl == "left_center"):
		doAngle(left_center_angle)

	elif(rsl == "center"):
		doAngle(center_angle)

	elif(rsl == "right_center"):
		doAngle(right_center_angle)

	elif(rsl == "right"):
		doAngle(right_angle)

	else:
		doAngle(0)

	time.sleep(1)

p.stop()
GPIO.cleanup()
