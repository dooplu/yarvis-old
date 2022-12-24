import widgets
import gestureRecognition
import cv2 as cv
import numpy as np
import time

screenWidth, screenHeight = 720, 480
outputImage = np.zeros((screenHeight, screenWidth, 3), np.uint8)

def fps(image, previousTime):
    font = cv.FONT_HERSHEY_SIMPLEX
    fps = 1/(time.time()-previousTime)
    fps = int(fps)
    fps = str(fps)
    cv.putText(image, fps, (5,35), font, 1,(255,255,255),2,cv.LINE_AA)

# organize all the drawing into its own function
def draw(image, landmarks, gesture):
    if gesture == 2:
        cv.circle(image, (landmarks[8][0], landmarks[8][1]), 10, (255,0,0), -1, cv.LINE_AA)
    if gesture == 3:
        image = np.zeros((screenHeight, screenWidth, 3), np.uint8)
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
    # pass the init variables into gesture recognition
    flag, debugImage, landmarks, currentGesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    if flag == 0:
        break

    
    outputImage = draw(outputImage, landmarks, currentGesture)
    fps(debugImage, previousTime)

    cv.imshow('debug', debugImage)
    cv.imshow('output', outputImage)

cap.release()
cv.destroyAllWindows()