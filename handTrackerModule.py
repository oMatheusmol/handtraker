import cv2
import time
import mediapipe as mp
import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon= 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands= self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms, self.mpHands.HAND_CONNECTIONS)
        return img     
    
    def findPosition (self, img, handNumber = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(myHand.landmark):
                    
                    height, width, channels = img.shape
                    positionX, positionY = int(lm.x*width), int(lm.y*height)
                    lmList.append([id,positionX, positionY])
                    if draw:
                        cv2.circle(img, (positionX, positionY), 5, (255,0,0), cv2.FILLED)
        return lmList

def main():
    pTime = 0
    cTime = 0
    cap= cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = handDetector()
    while True:
        sucess, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        # if len(lmList) != 0:
        #     print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,50),3)
        cv2.imshow("Hand Tracker Camera", img)
        cv2.waitKey(1)   

if __name__ == "__main__":
    main()