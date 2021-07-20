import json, numpy, time

from PIL import Image
from os import path
from picamera import PiCamera
from time import sleep

start_time = time.time()

contributionData = json.loads(open("/home/pi/Solargraphy/data/contributionData.json").read())
imageData = json.loads(open("data/imageData.json").read())
#  Detects the light intensity of each pixel in the bracketed image.
dim = contributionData["dim"]
bright = contributionData["bright"]


def highBurn(x):
    return dim[x]


def lowBurn(x):
    return bright[x]


def burn(img, type):
    g = None
    if type == 1:
        b = img.point(highBurn)
    else:
        b = img.point(lowBurn)

    # Save as 32 bit integer. Allows for values greater than 32 bits.
    return numpy.array(b, dtype=numpy.uint32)


camera = PiCamera()

camera.start_preview()

camera.shutter_speed = 1000 #
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/low.jpg')

camera.shutter_speed = 80000 #
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/high.jpg')

camera.stop_preview()

high = Image.open("/home/pi/Solargraphy/assets/high.jpg")
low = Image.open("/home/pi/Solargraphy/assets/low.jpg")
#Split channels
redH, greenH, blueH = Image.Image.split(high)
redL, greenL, blueL = Image.Image.split(low)

arrRed = burn(redL, 3) + burn(redH, 1)
arrGreen = burn(greenL, 3) + burn(greenH, 1)
arrBlue = burn(blueL, 3) + burn(blueH, 1)

if len(imageData["r"]) > 0:  # Image data already exists

    ogRed = numpy.array(imageData["r"])
    ogGreen = numpy.array(imageData["g"])
    ogBlue = numpy.array(imageData["b"])

    arrRed = numpy.add(arrRed, ogRed)
    arrGreen = numpy.add(arrGreen, ogGreen)
    arrBlue = numpy.add(arrBlue, ogBlue)


imageData["r"] = arrRed.tolist()#*0
imageData["g"] = arrGreen.tolist()#*0
imageData["b"] = arrBlue.tolist()#*0

imageDataW = open("data/imageData.json", "w+")
imageDataW.write(json.dumps(imageData))
imageDataW.close()

print("Done %s " % (time.time() - start_time))
