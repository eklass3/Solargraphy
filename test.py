from time import sleep

from picamera import PiCamera

camera = PiCamera()

camera.start_preview()

camera.shutter_speed = 1000 #
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/low.jpg')

camera.shutter_speed = 80000 #
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/high.jpg')

camera.stop_preview()