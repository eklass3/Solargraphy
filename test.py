from time import sleep
import json
from picamera import PiCamera

camera = PiCamera()

camera.start_preview()

camera.iso = 10 #800 Night
camera.shutter_speed = 100 # 20000 Night
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/low.jpg')

camera.shutter_speed = 1000 # 200000 Night
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/high.jpg')

camera.stop_preview()

imageData = json.loads(open("/home/pi/Solargraphy/data/imageData.json").read())

imageData["r"] = [0]
imageData["g"] = [0]
imageData["b"] = [0]

imageDataW = open("/home/pi/Solargraphy/data/imageData.json","w+")
imageDataW.write(json.dumps(imageData))
imageDataW.close()
