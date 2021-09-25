import cv2
import time
import numpy as np
import handTrackerModule as htm
import math

pTime = 0
cTime = 0
cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = htm.handDetector(detectionCon=0.8)

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1,y1= lmList[4][1], lmList[4][2]
        x2,y2= lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 6, (0,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 6, (0,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255) , 3)
        cv2.circle(img, (cx,cy),  6, (0,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)

        vol = np.interp(length, [10,160],[minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,50),3)
    cv2.imshow("Hand Tracker Camera", img)
    cv2.waitKey(1) 