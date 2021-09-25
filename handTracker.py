import cv2
import time
import mediapipe as mp
import numpy as np

cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
pTime = 0
mpHands = mp.solutions.hands
hands= mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    sucess, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                
                height, width, channels = img.shape
                positionX, positionY = int(lm.x*width), int(lm.y*height)
                print(id, positionX, positionY)
                # if id == 0:
                cv2.circle(img, (positionX, positionY), 15, (255,0,198), cv2.FILLED)
            mpDraw.draw_landmarks(img,handLms, mpHands.HAND_CONNECTIONS)

    cv2.putText(img, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,122),3)

    cv2.imshow("Hand Tracker Camera", img)
    cv2.waitKey(1)
