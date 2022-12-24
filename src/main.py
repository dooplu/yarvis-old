import widgets
import gestureRecognition
import cv2 as cv
import numpy as np

screenWidth, screenHeight = 720, 480
outputImage = np.zeros((screenHeight, screenWidth, 3), np.uint8)



cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init(1)

while True:

    flag, debugImage, landmarks, gesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    

    
    if flag == 0:
        break

    cv.imshow('debug', debugImage)
    cv.imshow('output', outputImage)

cap.release()
cv.destroyAllWindows()