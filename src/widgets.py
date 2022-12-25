import cv2 as cv
import numpy as np

class baseWidget:

    movementSmoothing = 0.15

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # linearly interpolate between two values
    def lerp(self, starting, ending, percentage):
        return int(starting + (ending - starting) * percentage)
    
    # given a target, move to said target with some smoothing
    def moveToTarget(self, x, y):
        self.x = self.lerp(self.x, x, baseWidget.movementSmoothing)
        self.y = self.lerp(self.y, y, baseWidget.movementSmoothing)
        


class circle(baseWidget):
    def __init__(self, x, y, radius, colour, thickness):
        super().__init__(x, y)
        self.radius = radius
        self.colour = colour
        self.thickness = thickness

    def display(self, image):
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)
    
    #def isGrabbed():
     #   return asd

    



