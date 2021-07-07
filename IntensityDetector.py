import json, numpy, time

from PIL import Image
from os import path
from Merger import Merger
from picamera import PiCamera
from time import sleep

start_time = time.time()

NUMBER_OF_MINUTES = 1

contributionData = json.loads(open("/home/pi/Solargraphy/data/contributionData.json").read())
#  Detects the light intensity of each pixel in the bracketed image.
dim = contributionData["dim"]
bright = contributionData["bright"]


def highBurn(x):
    return dim[x] / NUMBER_OF_MINUTES


def lowBurn(x):
    return bright[x] / NUMBER_OF_MINUTES


def burn(img, type):
    g = None
    if type == 1:
        #g = numpy.vectorize(highBurn)
        b = img.point(highBurn) 
    elif type == 2:
        g = numpy.vectorize(midBurn)
    else:
        #g = numpy.vectorize(lowBurn)
         b = img.point(lowBurn)
    
    
    #b = g(numpy.array(img))
    
    return numpy.array(b)


camera = PiCamera()

camera.start_preview()

camera.shutter_speed = 1500 #
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/low.jpg')

camera.shutter_speed = 80000 #
sleep(0.1)
camera.capture('/home/pi/Solargraphy/assets/high.jpg')

camera.stop_preview()

high = Image.open("/home/pi/Solargraphy/assets/high.jpg")
low = Image.open("/home/pi/Solargraphy/assets/low.jpg")

redH, greenH, blueH = Image.Image.split(high)
redL, greenL, blueL = Image.Image.split(low)

arrRed = burn(redL, 3) + burn(redH, 1) # + burn(redM, 2) + burn(redL, 3)
arrGreen = burn(greenL, 3) + burn(greenH, 1) # + burn(greenM, 2) + burn(greenL, 3)
arrBlue = burn(blueL, 3) + burn(blueH, 1) # + burn(blueM, 2) + burn(blueL, 3)

if path.exists("/home/pi/Solargraphy/assets/greyScale.png"):

    og = Image.open("/home/pi/Solargraphy/assets/greyScale.png")

    ogRed, ogGreen, ogBlue = Image.Image.split(og)

    arrRed += ogRed
    arrGreen += ogGreen
    arrBlue += ogBlue


finalRed = Image.fromarray(arrRed).convert("L")
finalGreen = Image.fromarray(arrGreen).convert("L")
finalBlue = Image.fromarray(arrBlue).convert("L")

rgb = numpy.dstack((finalRed, finalGreen, finalBlue))

imgFinal = Image.fromarray(rgb)
imgFinal.save("/home/pi/Solargraphy/assets/greyScale.png")

print("Done %s " % (time.time() - start_time))
