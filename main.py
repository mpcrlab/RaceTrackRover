from RoverExtended import *
from AIBrain import *
if __name__ == '__main__':
	path = raw_input("T for train, A for autonomous: ").upper()
	if path == "A":
		rover = AIBrain()
	else:
		rover = RoverExtended()