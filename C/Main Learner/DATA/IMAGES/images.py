from PIL import Image, ImageFilter
import numpy as np
import os

kernels = [(0,-1,0,-1,5,-1,0,-1,0)]
baseout = [0 for i in range(26)]

filew = open("HANDW.txt", "w")
line = ""

for imagename in os.listdir("./"):
    if imagename.endswith(".jpg") and imagename[1] == "2":
        imageR = Image.open(imagename)
        imageR = imageR.resize((40,40))

        for kernel in kernels:
            imageF = imageR.filter(ImageFilter.Kernel((3,3), kernel, 0.1, 0))
            #imageF = imageF.resize((40,40))
            imagedata = imageF.getdata()
            imagearray = np.array(imagedata)

            letter = ord(imagename[0])-97

            for pixel in imagearray:
                colour = float(pixel[0]+pixel[1]+pixel[2])/765.0

                line += str(colour) + ","

            baseout[letter] = 1
            line = line[:-1] + ":"

            for c in baseout:
                line += str(c) + ","
            
            line = line[:-1] + "\n"
            baseout[letter] = 0

        imageF.save("N" + imagename)

filew.write(line[:-1])
filew.close()