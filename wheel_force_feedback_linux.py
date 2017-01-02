from __future__ import print_function
import os

'''	
	This script fixes a problem with the MOMO Racing Wheel 
	that only happens on Linux operating systems (Mac not tested), 
	where the force feedback does not work. Although force feedback
	is not required to run RaceTrackRover, it still can be
	a hassle when training. 

	This problem is nonexistant on Windows machines.

	Requirements:
	- Have LTWheelConf installed: https://github.com/TripleSpeeder/LTWheelConf.git
'''


def getDeviceNumber(name):
	found = None

	output = os.popen('cat /proc/bus/input/devices')
	if output.readline() == '':
		print("Command not found")
		return None

	for line in output:
		if name in line:
			found = True
			break
	
	if not found:
		print(name, "not found")
		return None

	for line in output:
		if "H: Handlers=" in line:
			handler = line
			index = handler.index('event') # returns the index of 'e' in event
			index += 5 # account for length of event
			break
	
	output.close()

	number = ''
	while handler[index] != " ":
		number+=str(handler[index])
		index+=1

	return number

def getCommand():
	number = getDeviceNumber("HDA Intel PCH Headphone")
	if number:
		command = "ltwheelconf --wheel MR --altautocenter 100 --device /dev/input/event" + number
		print("Command:", command)
		return command

def fix():
	command = getCommand()
	if command:
		output = os.popen(command)