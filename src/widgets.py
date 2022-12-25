import cv2 as cv
import numpy as np
import math


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
        self.originalColour = colour
        self.thickness = thickness
        self.highlightBrightness = -40
        self.grabbingBefore = False
        self.highlightColour = (colour[0] + self.highlightBrightness, colour[1] + self.highlightBrightness, colour[2] + self.highlightBrightness)

    def display(self, image, cursorX, cursorY, gesture, gestureHistory):
        self.grab(cursorX, cursorY, gesture, gestureHistory)
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)
        
    
    def grab(self, cursorX, cursorY, currentGesture, gestureHistory):
        # we cant do anything if we have no data yet      
        if len(gestureHistory) < 1:
            return
        
        if self.grabbingBefore:
            if currentGesture == 1:
                self.moveToTarget(cursorX,cursorY)
                self.grabbingBefore = True
            else:
                self.grabbingBefore = False
        else:
            if math.dist((cursorX, cursorY), (self.x,self.y)) > self.radius:
                self.grabbingBefore = False
                return
            if currentGesture == 1:
                self.moveToTarget(cursorX,cursorY)
                self.grabbingBefore = True
            else:
                self.grabbingBefore = False
            

        
        
class cursor(baseWidget):
    def __init__(self, x, y, radius, colour, thickness):
        super().__init__(x, y)
        self.radius = radius
        self.colour = colour
        self.thickness = thickness
        
    def display(self, image):
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)
        

    



