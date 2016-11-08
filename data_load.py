import os
import cv2
import math
import numpy as np

folder_path = os.getcwd() + "/training_data"
def showdata(fname):
	cwd = os.getcwd()
	newpath = folder_path + "/" + fname + "/"
	frames = np.load(newpath + 'img.npy')
	angles = np.load(newpath + 'ang.npy')
	radius = 80
	i = 0
	for frame in frames:
	    angle = angles[i]
	    angle = angle * math.pi / 180
	    y = 240 - int(math.sin(angle) * radius)
	    x = int(math.cos(angle) * radius) + 160
	    #cv2.circle(frame, (160, 240), radius, (250, 250, 250), -1)
	    cv2.line(frame, (160, 240), (x, y), (0, 0, 0), 5)
	    font = cv2.FONT_HERSHEY_SIMPLEX
	    cv2.putText(frame, str(int(angle * 180 / math.pi)), (x, y), font, .8, (255, 0, 255), 2, cv2.LINE_AA)
	    cv2.imshow("Frame", frame)
	    cv2.waitKey(15)
	    i+=1

	cv2.destroyAllWindows()
def showAllData():
	files = os.listdir(folder_path)
	print files
	for file in files:
		showdata(file)

showAllData()