import os
import time
import numpy as np
class Data():
    def __init__(self):
        self.angles = []
        self.photos = []

    def load(self):
        # dir = raw_input('Enter the file name you would like to load?')
        # self.angles = np.loadtxt(dir)

    def save(self):
        directory =  os.getcwd()
        newpath = directory +"/Run " + str(time.time())
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        fname = newpath + "/ang"
        fname = str(fname)
        ang = np.array(self.angles, np.int32)
        np.savetxt(fname, ang)
        fname = newpath + "/img"
        fname = str(fname)
        pho = np.array(self.photos, np.int32)
        np.savetxt(fname, pho)