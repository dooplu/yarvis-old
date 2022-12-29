# not important anymore

import cv2 as cv
import numpy as np
import widgets

textSize = 0.4
thickness = 1
font = 0
text = "the quick brown fox jumps over the lazy dog"

positionX = 100
positionY = 100

image = np.zeros((480, 720, 3), np.uint8)





textWidth, textHeight = cv.getTextSize(text, font, textSize, thickness)
textBox = widgets.square()
cv.putText(image, text, (positionX, positionY), font, textSize, (255,255,255), thickness, 16)


cv.imshow("wordwrapping", image)
cv.waitKey(0)