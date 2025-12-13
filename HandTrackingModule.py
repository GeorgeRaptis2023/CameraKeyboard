import cv2
import mediapipe as mp
from threading import Thread
from typing import List

class handDetector:
    def __init__(self, mode=False, maxHands=2, comp=1, detectionCon=0.5, trackingCon=0.5):
        #confidence
        self.detectionCon=detectionCon
        self.trackingCon=trackingCon
        #constants
        self.mode=mode
        self.maxHands=maxHands
        self.size=7
        self.comp=comp
         #from cv
        self.mpHands=mp.solutions.hands
        self.Hands=self.mpHands.Hands(self.mode, self.maxHands, self.comp, self.trackingCon, self.trackingCon)
        self.mpDraw=mp.solutions.drawing_utils
        # Threaded capture
        self.cap = cv2.VideoCapture(0)
        self.ret, self.frame = self.cap.read()
        self.stopped = False
    # Thread functions
    def start(self):
        Thread(target=self.update, daemon=True).start()
        return self
    def update(self):
        while not self.stopped:
            self.ret,self.frame=self.cap.read()
    def read(self):return self.frame

    def stop(self):
        self.stopped=True
        self.cap.release()
    # Hand detection
    def findHands(self, img, draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.Hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True) -> List[List[int]]:
        PositionList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                PositionList.append([id, cx, cy])
                if draw:
                    cv2.circle(img,(cx,cy),self.size,(255, 255, 255),cv2.FILLED)
        return PositionList
