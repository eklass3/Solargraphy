import json, numpy

from PIL import Image
from os import path
from Merger import Merger
from picamera import PiCamera
from time import sleep


NUMBER_OF_MINUTES = 1

contributionData = json.loads(open("data/contributionData.json").read())
#  Detects the light intensity of each pixel in the bracketed image.


def highBurn(x):
    return contributionData["dim"][x]


def midBurn(x):
    return contributionData["mid"][x]


def lowBurn(x):
    return contributionData["bright"][x]


def burn(img, type):
    g = None
    if type == 1:
        g = numpy.vectorize(highBurn)
    elif type == 2:
        g = numpy.vectorize(midBurn)
    else:
        g = numpy.vectorize(lowBurn)

    return g(numpy.array(img))



camera = PiCamera()

camera.start_preview()

camera.shutter_speed = 1500
sleep(1)
camera.capture('/home/pi/Merger/assets/low.jpg')

# camera.shutter_speed = 3500
# sleep(1)
# camera.capture('/home/pi/Merger/assets/mid.jpg')

camera.shutter_speed = 6000
sleep(1)
camera.capture('/home/pi/Merger/assets/high.jpg')

camera.stop_preview()


high = Image.open("/home/pi/Merger/assets/high.jpg")
low = Image.open("/home/pi/Merger/assets/low.jpg")

redH, greenH, blueH = Image.Image.split(high)
redL, greenL, blueL = Image.Image.split(low)

arrRed = burn(redL, 3) + burn(redH, 1) # + burn(redM, 2) + burn(redL, 3)
arrGreen = burn(greenL, 3) + burn(greenH, 1) # + burn(greenM, 2) + burn(greenL, 3)
arrBlue = burn(blueL, 3) + burn(blueH, 1) # + burn(blueM, 2) + burn(blueL, 3)

if path.exists("/home/pi/Merger/assets/greyscale.png"):

    og = Image.open("/home/pi/Merger/assets/greyscale.png")

    ogRed, ogGreen, ogBlue = Image.Image.split(og)

    arrRed += ogRed
    arrGreen += ogGreen
    arrBlue += ogBlue


finalRed = Image.fromarray(arrRed).convert("L")
finalGreen = Image.fromarray(arrGreen).convert("L")
finalBlue = Image.fromarray(arrBlue).convert("L")

finalRed.save("/home/pi/Merger/assets/redGreyscale.png")
finalGreen.save("/home/pi/Merger/assets/greenGreyscale.png")
finalBlue.save("/home/pi/Merger/assets/blueGreyscale.png")

rgb = numpy.dstack((finalRed, finalGreen, finalBlue))

imgFinal = Image.fromarray(rgb)
imgFinal.save("/home/pi/Merger/assets/greyScale.png")

print("done")