import os
import sys

os.system('sudo ffmpeg -s 320x240 -i /dev/video0 http://localhost:8090/webcam.ffm')
