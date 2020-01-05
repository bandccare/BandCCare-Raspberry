import time
import sys
import os
import json
import requests
import threading

def start_Motion_Detect():
	os.system('lxterminal --command="python3 /home/pi/motion_detect.py"')

def start_FFmpeg():
	os.system('lxterminal --command="python /home/pi/play_ffmpeg.py"')

def start_Servo():
	os.system('lxterminal --command="python /home/pi/servo_control.py"')

def servo_init():
	os.system('lxterminal --command="python /home/pi/servo_init.py"')

t1 = threading.Thread(target = start_Motion_Detect)
t1.start()

time.sleep(1)

url_alarm = "http://192.168.0.3:5000/alarm"
response_alarm = requests.get(url=url_alarm)
j_alarm = response_alarm.json()
alarm = j_alarm["alarm"]

if(alarm == "alarm"):
	r = requests.post(url_alarm,data={'alarm':'noalarm'})

while True:
	url_alarm = "http://192.168.0.3:5000/alarm"
	response_alarm = requests.get(url=url_alarm)

	j_alarm = response_alarm.json()
	alarm = j_alarm["alarm"]

	print(alarm)

	if(alarm == "alarm"):

		os.system('sudo pkill -15 -ef motion_detect')
		print("motion_detect kill\n")

		time.sleep(0.5)

		t3 = threading.Thread(target = start_Servo)
		t3.start()
		t5 = threading.Thread(target = start_FFmpeg)
		t5.start()


		r = requests.post("http://192.168.0.3:5000/exit",data={'exit':'noexit'})

		while True:
			url_exit = "http://192.168.0.3:5000/exit"
			response_exit = requests.get(url=url_exit)

			j_exit = response_exit.json()
			exit = j_exit["exit"]

			print(exit)

			if(exit == "exit"):

				os.system('sudo pkill -15 -ef servo')
				time.sleep(0.5)

				with open("rsl.txt","w") as f:
					f.write("75.0")

				t7 = threading.Thread(target = servo_init)
				t7.start()

				time.sleep(4)

				os.system('sudo pkill -15 -ef play_ffmpeg')
				os.system('sudo pkill -15 -ef servo')
				time.sleep(0.5)

				t9 = threading.Thread(target = start_Motion_Detect)
				t9.start()

				url_alarm = "http://192.168.0.3:5000/alarm"
				response_alarm = requests.get(url=url_alarm)
				j_alarm = response_alarm.json()
				alarm = j_alarm["alarm"]

				print("reset: ",alarm," -> noalarm\n")

				if(alarm == "alarm"):
					r = requests.post(url_alarm,data={'alarm':'noalarm'})

				break

			time.sleep(1)
	time.sleep(1)
