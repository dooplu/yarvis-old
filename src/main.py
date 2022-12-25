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

glob = widgets.circle(0, 0, 50, (255, 255, 255))

def fps(image, previousTime):
    font = cv.FONT_HERSHEY_SIMPLEX
    fps = 1/(time.time()-previousTime)
    fps = int(fps)
    fps = str(fps)
    cv.putText(image, fps, (5,35), font, 1,(255,255,255),2,cv.LINE_AA)

# organize all the drawing into its own function
def draw(image, landmarks, gesture):
    if len(landmarks) < 1:
        return image
    # clear the frame
    image = np.zeros((screenHeight, screenWidth, 3), np.uint8)

    if gesture == 1:
        glob.x = int(lerp(glob.x, landmarks[9][0], 0.15))
        glob.y = int(lerp(glob.y, landmarks[9][1], 0.15))

    glob.display(image)
    return image

# linearly interpolate between two values
def lerp(starting, ending, percentage):
    return starting + (ending - starting) * percentage

# to smooth out noise and avoid sudden changes due to false positives
def smoothGesture(currentGesture, gestureHistory, smoothGestureThreshold):
    if len(gestureHistory) < 1:
        return 0
    smoothed = currentGesture
    counter = 0
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

# initialize the hand tracking and gesture recognition
cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init(1)

# main loop
while True:
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break
    # set the previous time to the current time at the beginning of the loop
    previousTime = time.time()
    # pass the init variables into gesture recognition
    flag, debugImage, landmarks, currentGesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    if flag == 0:
        break

    smoothedGesture = smoothGesture(currentGesture, gestureHistory, smoothGestureThreshold)
    
    outputImage = draw(outputImage, landmarks, smoothedGesture)
    #smoothedImage = draw(smoothedImage, landmarks, smoothedGesture)

    fps(debugImage, previousTime)
    gestureHistory.append(currentGesture)

    #cv.imshow('smoothed', smoothedImage)
    cv.imshow('debug', debugImage)
    cv.imshow('output', outputImage)

cap.release()
cv.destroyAllWindows()