import os
import cv2
import numpy as np

folder_path = os.getcwd() + "/training_data"
def showdata(fname):
	cwd = os.getcwd()
	newpath = folder_path + "/" + fname + "/"
	frames = np.load(newpath + 'img.npy')
	angles = np.load(newpath + 'ang.npy')

	i = 0
	for frame in frames:
	    angle = angles[i]
	    cv2.putText(frame, str(angle), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
	    cv2.imshow("Frame", frame)
	    cv2.waitKey(15)
	    i+=1

	cv2.destroyAllWindows()
def showAllData():
	files = os.listdir(folder_path)
	for file in files:
		showdata(file)

showAllData()