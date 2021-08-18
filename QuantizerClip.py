import json, numpy
from PIL import Image

imageData = json.loads(open("/home/pi/Solargraphy/data/imageData.json").read())

def quantize(arr):
    m = numpy.amax(arr)
    print(m)
    print(numpy.mean(arr))

    cutPoint = m / 2
    arr = numpy.clip(arr, 0, cutPoint)
    arr = (arr * numpy.true_divide(255, cutPoint))
    arr8 = arr.astype('uint8')

    return arr8


arrR = numpy.array(imageData["r"])
arrG = numpy.array(imageData["g"])
arrB = numpy.array(imageData["b"])

arrR8 = quantize(arrR)
arrG8 = quantize(arrG)
arrB8 = quantize(arrB)

rgb = numpy.dstack((arrR8, arrG8, arrB8))

finalImg = Image.fromarray(rgb)

finalImg.save("/home/pi/Solargraphy/assets/final.png")