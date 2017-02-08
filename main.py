from RoverExtended import *
from TFBrain import *
if __name__ == '__main__':
	path = raw_input("T for train, A for autonomous: ").upper()
	if path == "A":
	    rover = TFBrain()
	else:
	    rover = RoverExtended()
	rover.endSession()
