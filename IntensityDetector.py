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
        b = img.point(highBurn) 
    elif type == 2:
        b = img.point(midBurn) 
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

if path.exists("/home/pi/Solargraphy/assets/greyScale.png"):

    og = Image.open("/home/pi/Solargraphy/assets/greyScale.png")

    ogRed, ogGreen, ogBlue = Image.Image.split(og)
    
    ogRed = numpy.array(ogRed)
    ogGreen = numpy.array(ogGreen)
    ogBlue = numpy.array(ogBlue)
    
    arrRed = numpy.add(arrRed, ogRed)
    arrGreen = numpy.add(arrGreen, ogGreen)
    arrBlue = numpy.add(arrBlue, ogBlue)


print(numpy.amax(arrRed))
# Force array values to be from 0-255 despite being 32bit.
arrRed = numpy.clip(arrRed, 0, 255)
arrGreen = numpy.clip(arrGreen, 0, 255)
arrBlue = numpy.clip(arrBlue, 0, 255)

finalRed = Image.fromarray(arrRed)
finalGreen = Image.fromarray(arrGreen)
finalBlue = Image.fromarray(arrBlue)

finalRed.save("/home/pi/Solargraphy/assets/redFinal.png")

#Stack back channels
rgb = numpy.dstack((finalRed, finalGreen, finalBlue))
# Convert array type back to 8 bit (0-255)
rgb = rgb.astype(numpy.uint8)
# Create image, save
imgFinal = Image.fromarray(rgb)
imgFinal.save("/home/pi/Solargraphy/assets/greyScale.png")

print("Done %s " % (time.time() - start_time))
