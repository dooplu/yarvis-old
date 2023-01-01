# some notes:
# - I want to implement a whole widgetmanager/panel/screen class that would do alot of the drawing stuff for multiple widgets
# in the same place much more elegantly, but I'd like to actually finish this project
# - for v2, try not to do so much from scratch

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
        self.highlightColour = self.hightlightColour(colour)
        self.type = "base"
    
    def hightlightColour(self, colour):
        hightlightColour = []
        for i in range(len(colour)):
            hightlightColour.append(colour[i] + self.highlightBrightness)
        
        return hightlightColour

    # linearly interpolate between two values
    def lerp(self, starting, ending, percentage):
        return int(starting + (ending - starting) * percentage)
    
    # given a target, move to said target with some smoothing
    def moveToTarget(self, x, y):
        self.x = self.lerp(self.x, x, baseWidget.movementSmoothing)
        self.y = self.lerp(self.y, y, baseWidget.movementSmoothing)
    
    def grab(self, cursorX, cursorY, currentGesture):
        # figure out if the cursor is hovering ontop of the widget using the appropriate function
        if self.radius != 0: # if it has a radius not equal to zero
            self.hovering = self.isHoveringCircle(cursorX, cursorY)
        else: # otherwise its a rectangle
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
        # check if the cursor is within the circles radius
        if math.dist((cursorX, cursorY), (self.x, self.y)) < self.radius:
            self.colour = self.highlightColour
            return True 
        else:
            self.colour = self.originalColour
            return False

    def isHoveringSquare(self, cursorX, cursorY):
        # check if the cursor is within the bounds of the rectangle
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
        self.type = "circle"
        
    def display(self, image, cursorX, cursorY, gesture):
        self.grab(cursorX, cursorY, gesture)
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)


class square(baseWidget):
    def __init__(self, x, y, width, height, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.width = width
        self.height = height
        self.radius = 0 # this is so the grabbing function can identify which hover function to use
        self.type = "square"

    def display(self, image, cursorX, cursorY, currentGesture):
        # i prefer to use the center coordinates of the rectangl,e...
        # ... so we figure out the coordinates opencv wants with some math
        self.grab(cursorX, cursorY, currentGesture)
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
        self.highlightColour = self.hightlightColour(colour)
        self.type = "sticky"

    def display(self, image, cursorX, cursorY, gesture):
        lines = self.text.splitlines() # put text does not support new lines, so we split into individual lines
        lineSizes = [] # store the pixel widths of each line of text
        lineHeight = 0 
        for i in range(len(lines)): # find the pixel width of each line 
            size, baseline = cv.getTextSize(lines[i], self.font, self.fontSize, self.thickness)
            lineSizes.append(size[0])
            lineHeight = size[1] + baseline # add the baseline to the lineHeight, quirk with the getTextSize function

        longest = max(lineSizes) # find the widest amongst them as it will determine the postit width
        self.width = longest # we can use this for the grabbing functionnality
        self.height = lineHeight*len(lines) # this too
        self.grab(cursorX, cursorY, gesture) # now that we know the width and height, we can test for grabbing
        # the corners of the postit background rectangle
        topLeft = (self.x - (longest // 2 + postIt.margin), self.y - (self.height//2 + postIt.margin))
        bottomRight = (self.x + (longest // 2 + postIt.margin), self.y + self.height//2 + postIt.margin*2)

        # drawing the postit
        cv.rectangle(image, topLeft, bottomRight, self.colour, self.thickness, cv.LINE_AA) # background
        for i in range(len(lines)):
            line = lines[i] # current line in the iteration
            # the point at which to draw the text
            point = (self.x - lineSizes[i] // 2, topLeft[1] + postIt.margin + lineHeight * (i+1)) 
            cv.putText(image, line, point, self.font, self.fontSize, (255,255,255), 1, 16)
        
        
class cursor(baseWidget):
    def __init__(self, x, y, radius, colour, thickness):
        super().__init__(x, y, colour, thickness)
        self.radius = radius
   
    def display(self, image): # dont want the cursor to inherit all the grabbing stuff so it should have its own display function
        cv.circle(image, (self.x, self.y), self.radius, self.colour, self.thickness, cv.LINE_AA)