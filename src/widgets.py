import cv2 as cv
import numpy as np

class baseWidget:

    movementSmoothing = 0.15

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # linearly interpolate between two values
    def lerp(starting, ending, percentage):
        return starting + (ending - starting) * percentage
    
    def moveToTarget(self, x, y):
        self.x = self.lerp(self.x, x, baseWidget.movementSmoothing)
        self.y = self.lerp(self.y, y, baseWidget.movementSmoothing)
        


class circle(baseWidget):
    def __init__(self, x, y, radius, colour):
        super().__init__(x, y)
        self.radius = radius
        self.colour = colour

    def display(self, image):
        cv.circle(image, (self.x, self.y), self.radius, self.colour, -1, cv.LINE_AA)
        #return self.img
    
    #def isGrabbed():
     #   return asd

    



