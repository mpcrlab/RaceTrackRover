# RaceTrackRover

Seamlessly pick between Wheel and Keyboard to control the rover. Train the Brookstone Rover and gather data such as current frame and the wheel angle at that frame. Saves to a .NPY file to then be used to train a Neural Network.


##Note

Currently not supporting learning while in reverse, but can be used to navigate -- Frames will not be recorded when going in reverse at this time


##Wheel Information
The wheel outputs an angle between 0 and 180. Using Logitech's Momo Racing Force Feedback Wheel


####Controls
0: Farthest it can go to the RIGHT

90: Center and rover goes forward

180: Farthest it can go to the LEFT


###Wheel Button Layout

**Button 1:** Left handel under wheel
**Currently:** Toggle Lights

**Button 2:** Right handel under wheel
**Currently:** Display Battery Percentage

**Button 3:** Top left button
**Currently:** Toggle movement

**Button 4:** Top right button
**Currently:** Toggle Learning

**Button 5:** Middle left button
**Currently:** Erase 1 second of memory

**Button 6:** Middle right button
**Currently:** Erase 10 seconds of memory

**Button 7:** Bottom left button
**Currently:** Display saved frame count

**Buton 8:** Bottom right button
**Currently:** Saves data and Quits

**Button 9:** Gear shift pushed towards you
**Currently:** Toggle reverse

**Button 10:** Gear shift pushed away from you
**Currently:** Toggle reverse


##Keyboard Controls
  W: Forward

  A: Left

  S: Reverse

  D: Right

  Z: Ends program and save data
