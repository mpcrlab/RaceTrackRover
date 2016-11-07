import os
import cv2
import numpy as np

fname = raw_input("Enter Run Folder Name: ")
cwd = os.getcwd()
newpath = cwd + "/" + fname + "/"
frames = np.load(newpath + 'img.npy')
angles = np.load(newpath + 'ang.npy')

i = 0
for frame in frames:
    angle = angles[i]
    cv2.imshow("Frame", frame)
    cv2.waitKey(330)
    i+=1

cv2.destroyAllWindows()