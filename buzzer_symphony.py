from concurrent.futures import process
from re import M
import cv2
import numpy as np
import hand_detect as hd
import math
from boltiot import Bolt        
import conf 
import os
import mediapipe as mp
import json, requests
import time

from dotenv import load_dotenv
load_dotenv()
BOLT_API_KEY = os.getenv('API_KEY')
BOLT_DEVICE_ID = os.getenv('DEVICE_ID')



mybolt = Bolt(BOLT_API_KEY, BOLT_DEVICE_ID)

mode = False
volumeBar = 0

detector = hd.handDetector(detectionCon=0.7)
cap = cv2.VideoCapture(0)
# while True:
#     mybolt.digitalWrite('0', 'HIGH')
#     time.sleep(10)
#     mybolt.digitalWrite('0', 'LOW')
#     time.sleep(10)

while True:
    ret, frame = cap.read()
    detector.findHands(frame, draw = False)
    lmList = detector.findPosition(frame, draw = False)
   
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = ((x1+x2)//2), ((y1+y2)//2)
        
        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), -1)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), -1)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (219, 112, 147), 2)
        
        length = math.hypot(x2-x1, y2-y1)
        volumeBar = np.interp(length, [20,150], [400, 150])
        volume = np.interp(length, [20,150], [0, 255])
        
        if length < 20:
            cv2.circle(frame, (cx, cy), 10, (255, 255, 0), -1)
            
        cv2.rectangle(frame, (50, 150), (85, 400), (127, 255, 0), 3)
        cv2.rectangle(frame, (50, int(volumeBar)), (85, 400), (154, 250, 0), -1)
        
        if mode == True:
            mybolt.analogWrite('0', int(volume))
            print(mybolt.analogRead('0'))
            print(int(length), int(volume))
            mode = False
        #print(mybolt.analogRead('A0'))
        
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        mybolt.analogWrite('0',0)
        break

mybolt.digitalWrite('0','LOW')
# pin = 0
# data = mybolt.digitalWrite(pin)
# print (data)
cap.release() 
cv2.destroyAllWindows()

