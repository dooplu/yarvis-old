import widgets
import gestureRecognition
import cv2 as cv
import numpy as np

#screenWidth, screenHeight = 720, 480

#image = np.zeros((screenHeight, screenWidth, 3), np.uint8)



cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history = gestureRecognition.init(1)

while True:

    flag, image, landmarks, gesture = gestureRecognition.returnGestures(cap, hands, point_history, keypoint_classifier, point_history_classifier, history_length, finger_gesture_history)
    circles = []

    if gesture == 3:
        circles.append(widgets.circle(landmarks[8][0], landmarks[8][1], 5, (0, 0, 255)))
    
    if len(circles) > 0:
        for circle in circles:
            circle.display(image)

    if flag == 0:
        break

    cv.imshow('Hand Gesture Recognition', image)

cap.release()
cv.destroyAllWindows()