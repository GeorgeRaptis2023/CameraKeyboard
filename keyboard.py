from HandTrackingModule import handDetector
import pyautogui
import time
import math
import cv2
#function to detect click
def click(PositionList, threshold=30):
    #if fingers are detected and are close return True
    if len(PositionList)<9:return False
    return math.hypot(PositionList[4][1]-PositionList[8][1],PositionList[4][2]-PositionList[8][2])<threshold
def stopclick(PositionList,threshold=30):
    #if fingers are detected and are apart return True
    if len(PositionList)<9:return False
    return math.hypot(PositionList[4][1]-PositionList[8][1],PositionList[4][2]-PositionList[8][2])>threshold

detector = handDetector().start()
pTime=0
W,H=pyautogui.size()
smooth=5
prev_x,prev_y,pTime=0,0,0
ClickFlag=False
while True:
    img = detector.findHands(detector.read())
    PositionList = detector.findPosition(img)
    if len(PositionList) != 0:
        x,y=PositionList[8][1],PositionList[8][2]
        h,w,c=img.shape
        screen_x=prev_x+((x/w)*W-prev_x)/smooth
        screen_y=prev_y+((y/h)*H-prev_y)/smooth
        pyautogui.moveTo(screen_x,screen_y)
        prev_x, prev_y=screen_x,screen_y
        #So as to not click continiously
        if ClickFlag==False and click(PositionList):
            ClickFlag=True
            #pyautogui.click()
            print("click")
        elif ClickFlag==True and stopclick(PositionList):
            ClickFlag=False
    fps=1/(time.time()-pTime)
    pTime =time.time()
    cv2.imshow("Hand Mouse", img)
    if cv2.waitKey(1) & 0xFF==ord('c'):break

detector.stop()
cv2.destroyAllWindows()

