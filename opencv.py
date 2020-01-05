import cv2, pandas
import time
import requests
import os
import sys
import threading

static_back = None
motion_list = [None, None]
video = cv2.VideoCapture(0)

new_rec = 320

width = 0
height = 0
k=0
count_true=0
count_false=0

def postHtml(url, area):
	global count_true,count_false

	if (area != 0):
		count_true += 1
		print("count_true: ",count_true)
		if(count_true == 5):
			r = requests.post(url,data = {'detect':'true'})
			print(url,len(r.text),' send')
			count_true = 0
			count_false = 0
	else :
		count_false += 1
		print("count_false: ",count_false)
		if(count_false == 5):
			r = requests.post(url,data = {'detect':'false'})
        		print(url,len(r.text),' send')
			count_true = 0
			count_false = 0
	time.sleep(1)
	global k,width,height
	k=0
	width = 0
	height = 0

while True:
        check, frame = video.read()
        motion = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if static_back is None:
                static_back = gray
                continue

        diff_frame = cv2.absdiff(static_back, gray)
        thresh_frame = cv2.threshold(diff_frame, 160, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        (_, cnts, _) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                        continue

                motion = 1
               	(x,y,w,h) = cv2.boundingRect(contour)
               	cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

		new_rec = (2*x+w)/2
		#print(new_rec)
		width = x+w
		height = y+h

        motion_list.append(motion)
        motion_list = motion_list[-2:]

        cv2.imshow("Color Frame",frame)
	#cv2.imshow("Thresh_Frame",thresh_frame)
        #key = cv2.waitKey(1)

	with open("rsl.txt","w") as f:
		f.write("100")

	area = height*width

	if k == 0:
		k = 1
		t = threading.Thread(target = postHtml, args=('http://192.168.0.6:4000/detect', area))
		t.start()



video.release()
cv2.destoryAllWindows()
