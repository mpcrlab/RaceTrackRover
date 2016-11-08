import os
import time
import numpy as np

folder_path = os.getcwd() + "/training_data"
global all_frames
global all_angles
# allFrames = 
# allAngles = 
# global first
# first = True
# allFrames = allAngles = None

def getData(fname):
	newpath = folder_path + "/" + fname + "/"
	frames = np.load(newpath + 'img.npy')
	angles = np.load(newpath + 'ang.npy')
	if not all_frames:
		all_frames = frames
		all_angles = angles
	else:
		all_frames.append(frames)
		all_angles.append(angles)
	# allFrames.append(frames)
	# allAngles.append(angles)

def getFolderNames():
	files = os.listdir(folder_path)
	print files
	for file in files:
		getData(file)

# def save():
# 	getFolderNames()
# 	directory = os.getcwd()
# 	newpath = directory +"/all_data"
# 	if not os.path.exists(newpath):
# 		os.makedirs(newpath)
# 	fname = newpath + "/ang"
# 	# self.angles = np.array(self.angles, dtype=np.float)
# 	# np.savetxt(fname,self.angles)
# 	np.save(fname, allAngles)
# 	fname = newpath + "/img"
# 	np.save(fname, allFrames)
# 	print "Data saved!"

getFolderNames()
print len(all_frames)