import os, numpy, json
from PIL import Image


#
# Merges images together by using weighted averaging. Designed for merging longer exposure images (not the sun shots)
#

class Merger:
    #  Params: img1 - new image, img2 - merged image
    @staticmethod
    def merge(img1, img2, JSONPath):
        # Assuming all images are the same size, get dimensions of first image
        w, h = img1.size

        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        # Create a numpy array of floats to store the average (assume RGB images)
        arr = numpy.zeros((h, w, 4), numpy.float)

        # Load details about working merge image.
        mergedDetails = json.loads(open(JSONPath).read())

        # Convert images to floating point arrays
        imarrNew = numpy.array(img1, dtype=numpy.float)
        imarrMerge = numpy.array(img2, dtype=numpy.float)

        # Get total number of photos which have been merged into current working merge image
        totalStackPhotos = mergedDetails["mergeData"]["photoCount"]
        # Update merge image by applying proper weighted average
        arr = arr + numpy.average([imarrNew, imarrMerge], axis=0, weights=[1, totalStackPhotos])


        # Bound values in array and cast as 8-bit integer
        arr = numpy.array(numpy.round(arr), dtype=numpy.uint8)

        # Generate, save and preview
        out = Image.fromarray(arr, mode="RGBA")

        # Update working merge image json data file
        mergedDetails["mergeData"]["photoCount"] += 1
        mergedJSON = open(JSONPath, "w+")
        mergedJSON.write(json.dumps(mergedDetails))
        mergedJSON.close()

        return out
