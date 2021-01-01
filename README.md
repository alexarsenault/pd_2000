# pd_2000
Automated irrigation system project.

There's 3 main components to the main script irrigate.py:

1. take_picture - takes a picture using the raspberry pi camera
and returns the image filename of the picture taken

2. send_email - sends an email of the input picture in an automated
format with a pre-written message.

3. main - main function with infinite while loop that turns on
the GPIO pin for a few seconds every 10 hours. There's also an 
initialization sequence where the pump is pulsed 3 times so that 
it's known that the pump is on and has entered the main loop.


