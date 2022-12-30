import cv2 as cv
import numpy as np
import math

class baseWidget:

    movementSmoothing = 0.15

    def __init__(self, x, y, colour, thickness):
        self.x = x
        self.y = y
        self.grabbingBefore = False
        self.hovering = False
        self.colour = colour
        self.thickness = thickness
        self.originalColour = self.colour
        self.highlightBrightness = -40
        self.highlightColour = (self.colour[0] + self.highlightBrightness, self.colour[1] + self.highlightBrightness, self.colour[2] + self.highlightBrightness)
    
    # linearly interpolate between two values
    def lerp(self, starting, ending, percentage):
        return int(starting + (ending - starting) * percentage)
    
    # given a target, move to said target with some smoothing
    def moveToTarget(self, x, y):
        self.x = self.lerp(self.x, x, baseWidget.movementSmoothing)
        self.y = self.lerp(self.y, y, baseWidget.movementSmoothing)
    
    def grab(self, cursorX, cursorY, currentGesture):
        if self.radius != 0: # check if its a circluar widget
            self.circleGrab(cursorX, cursorY, currentGesture)
        else: # otherwise its a rectangular widget
            self.squareGrab(cursorX, cursorY, currentGesture)
        
    def circleGrab(self, cursorX, cursorY, currentGesture):
        self.hovering = self.isHoveringCircle(cursorX, cursorY)
        
    def squareGrab(self, cursorX, cursorY, currentGesture):
        self.hovering = self.isHoveringSquare(cursorX, cursorY)

        if self.hovering and self.grabbingBefore == False:
            if currentGesture == 1:
                self.grabbingBefore = True
                self.moveToTarget(cursorX, cursorY)
            else:
                self.grabbingBefore = False
        
        if currentGesture == 1 and self.grabbingBefore:
            self.moveToTarget(cursorX, cursorY)
        else:
            self.grabbingBefore = False
         
    def isHoveringCircle(self, cursorX, cursorY):
        if math.dist((cursorX, cursorY), (self.x, self.y)) < self.radius:
            self.colour = self.highlightColour
            return True
        else:
            self.colour = self.originalColour
            return False
    
    def isHoveringSquare(self, cursorX, cursorY):
        if cursorX > (self.x - self.width / 2) and cursorX < (self.x + self.width /2) and cursorY > (self.y - self.height / 2) and cursorY < (self.y + self.height /2):
            self.colour = self.highlightColour
            return True
        else:
            self.colour = self.originalColour
            return False


class circle(baseWidget):
    def __init__(self, x, y, radius, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.radius = radius
        
    def display(self, image, cursorX, cursorY, gesture, gestureHistory):
        self.grab(cursorX, cursorY, gesture)
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)


class square(baseWidget):
    def __init__(self, x, y, width, height, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.width = width
        self.height = height
        self.radius = 0

    def display(self, image):
        # to make things simpler, I want the coordinates to specify the center of the rectangle, so we do a little math
        pt1 = (int(self.x - self.width / 2), int(self.y - self.height / 2))
        pt2 = (int(self.x + self.width / 2), int(self.y + self.height / 2))
        cv.rectangle(image, pt1, pt2, self.colour, self.thickness, cv.LINE_AA)
    

class postIt(square):
    font = 0
    fontSize = 1
    fontThickness = 1
    margin = 5

    def __init__(self, text, x, y, colour):
        super().__init__(x, y, 0, 0, colour, -1)
        self.text = text
        self.originalColour = colour
        self.highlightBrightness = -40
        self.highlightColour = (colour[0] + self.highlightBrightness, colour[1] + self.highlightBrightness, colour[2] + self.highlightBrightness)

    def display(self, image, cursorX, cursorY, gesture):
        lines = self.text.splitlines() # put text does not support new lines, so we split into individual lines
        lineSizes = [] 
        lineHeight = 0
        for i in range(len(lines)): # find the pixel width of each line 
            size, baseline = cv.getTextSize(lines[i], self.font, self.fontSize, self.thickness)
            lineSizes.append(size[0])
            lineHeight = size[1] + baseline

        longest = max(lineSizes) # find the widest amongst them as it will determine the postit size, PIXELS
        self.width = longest
        self.height = lineHeight*len(lines)
        self.grab(cursorX, cursorY, gesture)
        # the corners of the rectangle 
        topLeft = (self.x - (longest // 2 + postIt.margin), self.y - (len(lines)*lineHeight//2 + postIt.margin))
        bottomRight = (self.x + (longest // 2 + postIt.margin), self.y + len(lines)*lineHeight//2 + postIt.margin)

        # drawing the postit
        cv.rectangle(image, topLeft, bottomRight, self.colour, self.thickness, cv.LINE_AA) # background
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
        

    



