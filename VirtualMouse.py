<<<<<<< HEAD
import time
from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np

import autopy

wCam, hCam = 640, 480
frmeR = 100

pTime = 0
plocx, ploxy = 0, 0
plocx, ploxy = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    seccess, img = cap.read()
    Hands, img = detector.findHands(img)
    # cek function hand lancmark
    if len(Hands):
        hand1 = Hands[0]
        lmList1 = hand1["lmlist"]  # list dari 21 landmark point
        bbox1 = hand1["bbox"]  # info dari index box x,y,w,h
        centerPoint1 = hand1["center"]  # titik tengah dari tangan cx, cy
        handType = hand1["type"]  # cek tangan right or left

    print(len(lmList1))
    cv2.imshow("image", img)
    cv2.waitKey(1)
=======
import time

import cv2
import HandTrackingModule as htm
import numpy as np

import autopy

wCam, hCam = 640, 480
frmeR = 100

pTime = 0
plocx, ploxy = 0, 0
plocx, ploxy = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxhands=2)
wscr, hscr = autopy.screen.size()

while True:
    seccess, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
>>>>>>> ce9694bf4a07c8e49328291285d1fa74b25a243f
