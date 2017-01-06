from RoverExtended import *
from AutonomousRover import *
if __name__ == '__main__':
	path = raw_input("T for train, A for autonomous: ").upper()
	if path == "A":
		rover = AutonomousRover()
	else:
		rover = RoverExtended()
	rover.endSession()