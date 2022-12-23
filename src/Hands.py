import cv2
import mediapipe as mp
import math
import numpy

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

maxPinchDist = 50

isPinchingNow = False
isPinchingBefore = False

rectCoords = []

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        roi = image
        image_height, image_width, _ = image.shape
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # print(
                #     f'Index finger tip coordinates: (',
                #     f'{int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)}, '
                #     f'{int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)}), '
                #     f'Thumb finger tip coordinates: (',
                #     f'{int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width)}, '
                #     f'{int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height)})'
                # )
                # Assign the index and thumb positions to these variables for ease of use
                indexPos = [int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width),
                            int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)]
                thumbPos = [int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width),
                            int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height)]

                # Find distance between thumb tip and index tip
                dist = math.sqrt(((indexPos[0] - thumbPos[0]) ** 2) + ((indexPos[1] - thumbPos[1]) ** 2))

                # If the index and thumb are close enough to one another, we can conclude the user is pinching
                if dist < maxPinchDist:
                    # print("Pinching!")
                    # text = 'Pinching'
                    isPinchingNow = True
                    # Determine the average location
                    avgPoint = (int((indexPos[0] + thumbPos[0]) / 2), int((indexPos[1] + thumbPos[1]) / 2))
                    # print(avgPoint)
                else:
                    # print('Not Pinching!')
                    # text = 'Not Pinching'
                    isPinchingNow = False

                # Determine if the user has begun pinching as a result of the previous frames pinching being false
                if isPinchingNow == True and isPinchingBefore == False:
                    # print("Started Pinching")
                    firstPoint = avgPoint  # Assign the point at which the user starting pinching
                if isPinchingNow == True and isPinchingBefore == True:
                    lastPoint = avgPoint
                # Determine if the user has stopped pinching as a result of the previous frames pinching being true
                elif isPinchingNow == False and isPinchingBefore == True:
                    # print("Stopped Pinching")
                    lastPoint = avgPoint  # Assign the point at which the user stopped
                # print(isPinchingBefore, isPinchingNow)

                # Only add points to list if there are points to create rectangles from
                if 'firstPoint' in locals() and 'lastPoint' in locals():
                    rectCoord = (firstPoint, lastPoint)
                    rectCoords.append(rectCoord)

                # cv2.putText(image, text, (indexPos), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2)

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Go through list of points and make rectangles
        for rectCoord in rectCoords:
            if lastPoint > firstPoint:
                roi = image[firstPoint[1]:lastPoint[1], firstPoint[0]:lastPoint[0]]
            else:
                roi = image[lastPoint[1]:firstPoint[1], lastPoint[0]:firstPoint[0]]
            cv2.rectangle(image, firstPoint, lastPoint, (255, 0, 0), 3)

        isPinchingBefore = isPinchingNow

        roiHeight, roiWidth, _ = roi.shape
        roiPadded = cv2.copyMakeBorder(roi, 0, image_height - roiHeight, 0, image_width - roiWidth, cv2.BORDER_CONSTANT)
        #roiPadded = cv2.resize(roi, (image_width, image_height))
        final = numpy.concatenate((image, roiPadded), axis=1)
        cv2.imshow('Iron Man', final)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
