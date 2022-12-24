import widgets
import gestureRecognition
import cv2 as cv
import numpy as np

#screenWidth, screenHeight = 720, 480

#image = np.zeros((screenHeight, screenWidth, 3), np.uint8)

circle1 = widgets.circle(200, 200, 50, (255, 255, 255))


cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init()

while True:

    flag, image = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    if flag == 0:
        break

    cv.imshow('Hand Gesture Recognition', image)

cap.release()
cv.destroyAllWindows()