import os
import time
import numpy as np
class Data():
    def __init__(self):
        self.angles = []
        self.photos = []

    def load(self):
        pass

    def save(self):
        directory =  os.getcwd()
        newpath = directory +"/Run " + str(time.time())
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        fname = newpath + "/ang"
        # self.angles = np.array(self.angles, dtype=np.float)
        # np.savetxt(fname,self.angles)
        np.save(fname, self.angles)
        fname = newpath + "/img"
        np.save(fname,self.photos)
        print "Data saved!"