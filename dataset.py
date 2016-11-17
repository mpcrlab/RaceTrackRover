import os
import time
import numpy as np
import math
import cv2

#file path with all the Run data
training = os.getcwd() + "/training_data"

#folder name for where to output the combined/merged data
combined = os.getcwd() + "/dataset"

#helper function, returns frames and angles given a folder name
def getData(fname):
	newpath = training + "/" + fname + "/"
	frames = np.load(newpath + 'img.npy')
	angles = np.load(newpath + 'ang.npy')
	return frames, angles

#writes frames and angles to seperate npy files inside fname folder
def writeData(frames, angles, fname):
	directory = os.getcwd()
	newpath = fname
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	fname = newpath + "/img.npy"
	np.save(fname, frames)
	fname = newpath + "/ang.npy"
	np.save(fname, angles)
	print "Data saved!"

#loops through all training data lists and combines into single numpy lists
def getAllData():
	files = os.listdir(training)
	all_angles = np.array([])
	all_frames = np.array([[[[]]]])
	for file in files:
		frames, angles = getData(file)
		all_angles = np.concatenate([all_angles, angles])
		all_frames = np.vstack([all_frames,frames]) if all_frames.size else frames
	return all_frames, all_angles

#call this function to merge all data 
def writeEntireDataset(fname):
	all_frames, all_angles = getAllData()
	writeData(all_frames,all_angles, fname)

#parameter
def displayData(frames, angles, show_angles=True):
	radius = 80
	i = 0
	for frame in frames:
		if show_angles:
		    angle = angles[i]
		    angle = angle * math.pi / 180
		    y = 240 - int(math.sin(angle) * radius)
		    x = int(math.cos(angle) * radius) + 160
		    #cv2.circle(frame, (160, 240), radius, (250, 250, 250), -1)
		    cv2.line(frame, (160, 240), (x, y), (0, 0, 0), 5)
		    font = cv2.FONT_HERSHEY_SIMPLEX
		    cv2.putText(frame, str(int(angle * 180 / math.pi)), (x, y), font, .8, (255, 0, 255), 2)
		cv2.imshow("Frame", frame)
		cv2.waitKey(15)
		i+=1

	cv2.destroyAllWindows()

#show_angles bool to show angle needle when displaying
def displayTraining(show_angles=True):
	files = os.listdir(training)
	print files
	for file in files:
		frames, angles = getData(file)
		displayData(frames, angles)

def displayCombined(show_angles=True):
	path = combined + "/"
	frames = np.load(path + 'img.npy')
	angles = np.load(path + 'ang.npy')
	displayData(frames, angles)


input = raw_input("Press M to merge training dataset to single file, D to display a single Run file, or SPACE to display entire dataset (M/D/SPACE):").upper()
if input == 'M':
	if not os.path.exists(combined):
		writeEntireDataset(combined)
elif input == 'D':
	fname = raw_input("Paste the run file name here: ")
	frames, angles = getData(fname)
	displayData(frames, angles, False)
else:
	if os.path.exists(combined):
		displayCombined()
	else:
		writeEntireDataset(combined)
		displayCombined()

