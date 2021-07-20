import json, time, numpy
from PIL import Image

imageData = json.loads(open("data/imageData.json").read())

def quantize(arr):
    max = numpy.amax(arr)

    arr8 = (arr * (255 / max)).astype('uint8')

    return arr8


arrR = numpy.array(imageData["r"])
arrG = numpy.array(imageData["g"])
arrB = numpy.array(imageData["b"])

arrR8 = quantize(arrR)
arrG8 = quantize(arrG)
arrB8 = quantize(arrB)

rgb = numpy.dstack((arrR8, arrG8, arrB8))

finalImg = Image.fromarray(rgb)

finalImg.save("assets/greyScale.png")