# Importing the basic dependencies
import os
import cv2
import mediapipe as mp
import time

# WEbcam capture
cap = cv2.VideoCapture(0)

# mp Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

# Visualizing
while True:
    # Frame by frame reading
    ret, frame = cap.read()

    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    results = hands.process(frame_RGB)

    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLmrks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLmrks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # If we want to specifically detect and track the tip of our thumb, we can do that:
                if id == 4:
                    cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(frame, handLmrks, mpHands.HAND_CONNECTIONS) # until here is for detecting and drawing 


    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime
    cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (255, 225, 0), 3)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()