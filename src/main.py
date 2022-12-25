import widgets
import gestureRecognition
import cv2 as cv
import numpy as np
import time
from collections import deque

screenWidth, screenHeight = 720, 480
outputImage = np.zeros((screenHeight, screenWidth, 3), np.uint8)
#smoothedImage = np.zeros((screenHeight, screenWidth, 3), np.uint8)
gestureHistory = deque(maxlen=10)
smoothGestureThreshold = 0.5

glob = widgets.circle(0, 0, 25, (255, 255, 255))

def fps(image, previousTime):
    font = cv.FONT_HERSHEY_SIMPLEX
    fps = 1/(time.time()-previousTime)
    fps = int(fps)
    fps = str(fps)
    cv.putText(image, fps, (5,35), font, 1,(255,255,255),2,cv.LINE_AA)

# creates a blank frame 
def clearFrame():
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
def draw(image, landmarks, gesture):
    # clear the frame at the beginning of every draw loop
    image = clearFrame()

    return image



# initialize the hand tracking and gesture recognition
cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init(1)

# main loop
while True:
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break
    # set the previous time to the current time at the beginning of the loop
    previousTime = time.time()
    # pass the init variables into gesture recognition, this returns hand gesture, landmark coordinates and the latest camera frame
    flag, debugImage, landmarks, currentGesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    if flag == 0:
        break

    # pass the currentGesture into this smoothedGesture function so that we can reduce false positives messing with manipulation
    smoothedGesture = smoothGesture(currentGesture, gestureHistory, smoothGestureThreshold)
    
    # pass the frame through the draw loop and return it
    outputImage = draw(outputImage, landmarks, smoothedGesture)
    #smoothedImage = draw(smoothedImage, landmarks, smoothedGesture)

    # add fps to the debug image, BROKEN
    fps(debugImage, previousTime)

    # track the last x gestures (as set by gestureHistory maxlen) to be used by smoothedGesture as well as others
    gestureHistory.append(currentGesture)

    #cv.imshow('smoothed', smoothedImage)
    cv.imshow('debug', debugImage)
    cv.imshow('output', outputImage)

cap.release()
cv.destroyAllWindows()