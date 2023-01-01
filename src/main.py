import widgets
import gestureRecognition
import cv2 as cv
import numpy as np
import time
from collections import deque
from utils import CvFpsCalc
import os

screenWidth, screenHeight = 720, 480
outputImage = np.zeros((screenHeight, screenWidth, 3), np.uint8)
gestureHistory = deque(maxlen=10) # deques are great because it erases the oldest element and shifts everythign over to the left
drawQueue = []
smoothGestureThreshold = 0.5 # play with this, affects gesture smoothing

cvFpsCalc = CvFpsCalc(buffer_len=10)

cursor = widgets.cursor(0, 0, 15, (255, 146, 74), 3)

# creates a blank frame 
def clearFrame(image):
    image = np.zeros((screenHeight, screenWidth, 3), np.uint8)
    return image

# to smooth out noise and avoid sudden changes due to false positives
def smoothGesture(currentGesture, gestureHistory, smoothGestureThreshold):
    if len(gestureHistory) < 1:
        return 0
    smoothed = currentGesture
    gesturePresences = {}
    for gesture in gestureHistory:
        if gesture not in gesturePresences:
            gesturePresences[gesture] = 0      
        gesturePresences[gesture]  = gesturePresences[gesture] + 1
    
    currentGesturePresence = gesturePresences.get(currentGesture, 0) / len(gestureHistory) 

    if currentGesturePresence >= smoothGestureThreshold:
        smoothed = currentGesture
    else:
        for key in gesturePresences:
            if gesturePresences[key] == max(gesturePresences.values()):
                smoothed = key
                break

    return smoothed


# organize all the drawing into its own function
def draw(image, cursorX, cursorY, gesture, gestureHistory):
    # clear the frame at the beginning of every draw loop
    image = clearFrame(image)
    if os.path.exists(".\save\sticky.txt"):
        drawQueue.append(createNote()) # create a new note if one has been created by the voice assistant

    if len(drawQueue) > 0:
        for widget in drawQueue:
            widget.display(image, cursorX, cursorY, gesture)

    drawCursor(image, cursorX, cursorY)
    return image

def drawCursor(image, cursorX, cursorY):
    cursor.moveToTarget(cursorX, cursorY)
    #cursor.x = widgets.baseWidget.lerp(cursor.x, cursorX, widgets.baseWidget.movementSmoothing)
    #cursor.y = widgets.baseWidget.lerp(cursor.y, cursorY, widgets.baseWidget.movementSmoothing)
    cursor.display(image)

# we might want to change what defines our cursor in the future so its convenient to put this into its own function
def returnCursor(landmarks):
    if len(landmarks) < 1:
        return int(screenWidth/2), int(screenHeight/2)
    cursorX = (landmarks[8][0] + landmarks[4][0]) / 2
    cursorY = (landmarks[8][1] + landmarks[4][1]) / 2
    cursorX = int(cursorX)
    cursorY = int(cursorY)
    return cursorX, cursorY # the point halfway between the thumb and index

def drawFps(image, fps):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
            1.0, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
            1.0, (255, 255, 255), 2, cv.LINE_AA)

def createNote():
    note = None
    with open(".\save\sticky.txt") as file:
        parameters = file.read().splitlines() # every line of the file is a paramter
        text = parameters[0] # first line is the text of the note
        colour = parameters[1].split(",") # the second is the colour for the background

        text = text.split(" ") # turn the text string into an array demarkated by the spaces...
        string = ""
        for i in range(len(text)): # ... we do this because we want to recognize the command for a new line, and replace it accordingly
            word = text[i]
            if word == "new" and text[i+1] == "line": 
                string += "\n"
                continue
            elif word == "line" and text[i-1] == "new":
                continue 
            string += word + " "
        
        colour = list(map(int, colour)) # the variable colour is a list of strings, we need to cast each element as an integer

        note = widgets.postIt(string, screenWidth//2, screenHeight//2, colour) # create a new postit object and assign it to this variable
    os.remove(".\save\sticky.txt") # when we're done getting the info from the file, delete it
    return note # return this note to be used in the draw queue

def saveWidgets():
    with open(".\save\save.txt", "w") as file:
        string = ""
        for widget in drawQueue:
            if widget.type == "sticky":
                string += widget.type
                string += "\n"
                string += widget.text
                string += "\n"
                string += "{}, {}".format(widget.x, widget.y)
                string += "\n"
                string += "{}, {}, {}".format(widget.colour[0], widget.colour[1], widget.colour[2])
                string += "\n\n"
        
        file.write(string)

# initialize the hand tracking and gesture recognition
cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init(1)

# main loop
while True:
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break
    # pass the init variables into gesture recognition, this returns hand gesture, landmark coordinates and the latest camera frame
    flag, debugImage, landmarks, currentGesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    if flag == 0:
        break

    # 
    cursorX, cursorY = returnCursor(landmarks)
    ####################################################################################################
    fps = cvFpsCalc.get()

    # pass the currentGesture into this smoothedGesture function so that we can reduce false positives messing with manipulation
    smoothedGesture = smoothGesture(currentGesture, gestureHistory, smoothGestureThreshold)
    
    # pass the frame through the draw loop and return it
    outputImage = draw(outputImage, cursorX, cursorY, smoothedGesture, gestureHistory)
    #smoothedImage = draw(smoothedImage, landmarks, smoothedGesture)
    
    #fps function
    drawFps(debugImage, fps)

    # track the last x gestures (as set by gestureHistory maxlen) to be used by smoothedGesture as well as others
    gestureHistory.append(currentGesture)
    #print(gestureHistory)
    #cv.imshow('smoothed', smoothedImage)
    cv.imshow('debug', debugImage)
    cv.imshow('output', outputImage)

cap.release()
cv.destroyAllWindows()

saveWidgets()