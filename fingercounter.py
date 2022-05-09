import cv2
import time
import HandTrackingModule as htm
from cvzone.SerialModule import SerialObject 


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
uno=SerialObject()
tipIds = [4, 8, 12, 16, 20]
 
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
 
    if len(lmList) != 0:
        fingers = []
 
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
 
        # 4 Fingers
        for id in range(1, 5):
            if (lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
 
        # print(fingers)

        totalFingers = fingers.count(1)
        # print(totalFingers)
        cv2.rectangle(img,(20,40),(60,100),(0,0,0),cv2.FILLED)
        cv2.putText(img, str(totalFingers), (20, 90), cv2.FONT_ITALIC,
                    2, (0, 0, 255), 8)
        if totalFingers==0:
            uno.sendData([1,1])
        elif totalFingers==1:
            uno.sendData([1,2])
        elif totalFingers==2:
            uno.sendData([1,3])
        elif totalFingers==3:
            uno.sendData([1,4])
        elif totalFingers==4:
            uno.sendData([1,5])
        elif totalFingers==5:
            uno.sendData([1,6]) 
            
        
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (500, 30), cv2.FONT_HERSHEY_PLAIN,2, (0,0,255), 3)

    cv2.imshow("Image", img)
    if ord('q')==cv2.waitKey(1):
        break;