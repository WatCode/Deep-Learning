from PIL import Image, ImageFilter
import numpy as np

filer = open("ARRAY.txt", "r").read()

imagelist = [[float(j) for j in i.split(",")] for i in filer.split("\n")]
imagearray = np.array(imagelist)

imageW = Image.fromarray(imagearray)
imageW = imageW.convert("RGB")
imageW.save("Narray.jpg")