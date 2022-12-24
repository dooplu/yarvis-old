import cv2 as cv
import numpy as np

class object:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class circle(object):
    def __init__(self, x, y, radius, colour):
        super().__init__(x, y)
        self.radius = radius
        self.colour = colour

    def display(self, image):
        cv.circle(image, (self.x, self.y), self.radius, self.colour, -1, cv.LINE_AA)
        #return self.img



