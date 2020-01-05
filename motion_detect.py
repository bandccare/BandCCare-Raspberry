from imutils.video import VideoStream
import imutils
import time
import cv2

saliency = None
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=150)

	if saliency is None:
		#Wang이 만든 Saliency motion 메소드 사용해 객체 인스턴스화 시킴
		saliency = cv2.saliency.MotionSaliencyBinWangApr2014_create()
		#saliency 이미지 크기 정함 (너비,높이)
		saliency.setImagesize(frame.shape[1], frame.shape[0])
		#saliency 초기화
		saliency.init()

	#frame을 회색 음영처리
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#음영처리된 frame을 배경과 사물을 분리시킬수 있도록 계산
	#돌출맵이 계산되고 있으면 true 아니면 false
	(success, saliencyMap) = saliency.computeSaliency(gray)
	#돌출된 값을 saliencyMap에 씌움(frame 전체에)
	saliencyMap = (saliencyMap * 255).astype("uint8")

	(_, cnts, _) = cv2.findContours(saliencyMap.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour) < 100:
			continue
		(x,y,w,h) = cv2.boundingRect(contour)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)

	#전체크기 가로:150,세로:112
	rec_x = x+w/2
	print("x:",rec_x)
	cv2.imshow("Frame", frame)
	cv2.imshow("Map", saliencyMap)

	with open("rsl.txt","w") as f:
		f.write(str(rec_x))

	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

vs.stop()
cv2.destroyAllWindows()
