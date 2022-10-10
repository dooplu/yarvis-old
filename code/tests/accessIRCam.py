import numpy as np
import cv2 as cv

capture = cv.VideoCapture(-1)
if not capture.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = capture.read()

    if not ret:
        print("Cannot receive frame. Exiting...")
        break
    
    cv.imshow('Camera', frame)
    if cv.waitKey(1) == ord('q'):
        break

capture.release()
cv.destroyAllWindows()