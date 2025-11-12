# Import packages
import cv2
import mediapipe as mp
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Import the hand tracking module we made
import HandTrackingModule as htm


# Parameters
############################
wCam, hCam = 1000, 565
pTime = 0

# Webcam capture
############################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon = 0.7)

# PyCaw Audio connection
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# volume.GetMute()
# volume.GetMasterVolumeLevel()

vol_range = volume.GetVolumeRange()

vol = 0
volBar = 400
volPercent = 0
min_vol = vol_range[0]
max_vol = vol_range[1]

# Visualization
while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw= False)


    if len(lmlist) != 0:
        # print(lmlist[4], lmlist[8]) 
        # 4 - Thumb tip, 8 - Index finger tip


        # Locations of thumb and index tip, and the centre of the line joining them
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
 
        cv2.circle(frame, (x1,y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2,y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (cx,cy), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

        # Distance between index and thumb
        length = math.hypot(x2-x1, y2-y1)

        # print(length)
    
        # Hand range 20 - 300
        # Volume range -96 to 0

        vol = np.interp(length, [40, 320], [min_vol, max_vol])
        volBar = np.interp(length, [40, 320], [400, 150]) 
        volPercent = np.interp(length, [40, 320], [0, 100]) 
        

        # print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None) 

        if length < 50:
            cv2.circle(frame, (cx,cy), 15, (0, 255, 0), cv2.FILLED)
    
    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(frame, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, f"{int(volPercent)} %", (40, 450),  cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)


    # FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS: {str(int(fps))}", (10, 40),  cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()