import cv2 as cv
import numpy as np
from lib import widgets

screenWidth, screenHeight = 720, 480

image = np.zeros((screenHeight, screenWidth, 3), np.uint8)

circle1 = widgets.circle(200, 200, 50, (255, 255, 255))

def draw():
    image = np.zeros((screenHeight, screenWidth, 3), np.uint8) # clear the frame
    #cv.circle(image, (100, 100), 50, (255,255,255), -1, cv.LINE_AA)
    circle1.display(image)
    cv.imshow("Image", image)


while True:
    
    draw()
    
    keyPressed = cv.waitKeyEx(25)
    if keyPressed == 27:
        break
    


