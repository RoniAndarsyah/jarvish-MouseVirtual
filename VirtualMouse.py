import time

import cv2
import pyHandTrackingModule as htm
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
