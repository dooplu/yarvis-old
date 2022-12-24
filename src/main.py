import widgets
import gestureRecognition
import cv2 as cv
import numpy as np
import time

screenWidth, screenHeight = 720, 480
outputImage = np.zeros((screenHeight, screenWidth, 3), np.uint8)

font = cv.FONT_HERSHEY_SIMPLEX

previousTime = 0



cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init(1)

while True:

    flag, debugImage, landmarks, gesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    

    
    if flag == 0:
        break

    
    fps = 1/(time.time()-previousTime)
    fps = int(fps)
    fps = str(fps)
    previousTime = time.time()
    
    cv.putText(debugImage, fps, (5,35), font, 1,(255,255,255),2,cv.LINE_AA)
    cv.imshow('debug', debugImage)
    cv.imshow('output', outputImage)

cap.release()
cv.destroyAllWindows()