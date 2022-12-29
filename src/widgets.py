import cv2 as cv
import numpy as np
import math


class baseWidget:

    movementSmoothing = 0.15

    def __init__(self, x, y, colour, thickness):
        self.x = x
        self.y = y
        self.colour = colour
        self.thickness = thickness
    
    # linearly interpolate between two values
    def lerp(self, starting, ending, percentage):
        return int(starting + (ending - starting) * percentage)
    
    # given a target, move to said target with some smoothing
    def moveToTarget(self, x, y):
        self.x = self.lerp(self.x, x, baseWidget.movementSmoothing)
        self.y = self.lerp(self.y, y, baseWidget.movementSmoothing)
        


class circle(baseWidget):
    def __init__(self, x, y, radius, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.radius = radius
        self.originalColour = self.colour
        self.highlightBrightness = -40
        self.grabbingBefore = False
        self.highlightColour = (self.colour[0] + self.highlightBrightness, self.colour[1] + self.highlightBrightness, self.colour[2] + self.highlightBrightness)

    def display(self, image, cursorX, cursorY, gesture, gestureHistory):
        self.grab(cursorX, cursorY, gesture)
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)
        
    
    def grab(self, cursorX, cursorY, currentGesture):
        
        if self.grabbingBefore:
            if currentGesture == 1:
                self.moveToTarget(cursorX,cursorY)
                self.colour = self.highlightColour
                self.grabbingBefore = True
            else:
                self.colour = self.originalColour
                self.grabbingBefore = False
        else:
            if math.dist((cursorX, cursorY), (self.x,self.y)) > self.radius:
                self.colour = self.originalColour
                self.grabbingBefore = False
                return
            if currentGesture == 1:
                self.colour = self.highlightColour
                self.moveToTarget(cursorX,cursorY)
                self.grabbingBefore = True
            else:
                self.colour = self.originalColour
                self.grabbingBefore = False
            
class square(baseWidget):
    def __init__(self, x, y, width, height, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.width = width
        self.height = height

    def display(self, image):
        # to make things simpler, I want the coordinates to specify the center of the rectangle, so we do a little math
        pt1 = (int(self.x - self.width / 2), int(self.y - self.height / 2))
        pt2 = (int(self.x + self.width / 2), int(self.y + self.height / 2))
        cv.rectangle(image, pt1, pt2, self.colour, self.thickness, cv.LINE_AA)
    

class postIt(square):
    font = 0
    fontSize = 0.5
    fontThickness = 1
    margin = 5

    def __init__(self, text, x, y, colour):
        super().__init__(x, y, 0, 0, colour, -1)
        self.text = text
    
    def display(self, image):
        lines = self.text.splitlines() # put text does not support new lines, so we split into individual lines
        lineSizes = [] 
        lineHeight = 0
        for i in range(len(lines)): # find the pixel width of each line 
            size, baseline = cv.getTextSize(lines[i], self.font, self.fontSize, self.thickness)
            lineSizes.append(size[0])
            lineHeight = size[1] + baseline

        longest = max(lineSizes) # find the widest amongst them as it will determine the postit size, PIXELS
       #widestIndex = lineSizes.index(longest)
        #widestLine = lines[widestIndex] # the widest line determines the width of the postIt, STRING
        
        # the corners of the rectangle 
        topLeft = (self.x - (longest // 2 + postIt.margin), self.y - (len(lines)*lineHeight//2 + postIt.margin))
        bottomRight = (self.x + (longest // 2 + postIt.margin), self.y + len(lines)*lineHeight//2 + postIt.margin)

        cv.rectangle(image, topLeft, bottomRight, self.colour, self.thickness, cv.LINE_AA)
        for i in range(len(lines)):
            line = lines[i]
            point = (self.x - lineSizes[i] // 2, topLeft[1] + postIt.margin + lineHeight * (i+1))

            cv.putText(image, line, point, self.font, self.fontSize, (255,255,255), 1, 16)



        


        
class cursor(baseWidget):
    def __init__(self, x, y, radius, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.radius = radius
   
    def display(self, image):
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)
        

    



