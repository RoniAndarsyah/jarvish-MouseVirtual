import math
import time
import cv2
import mouse
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# set cam
wCam, hCam = 640, 480
frameR = 90
smoothing = 4

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector(detectionCon=0.5, maxHands=2)
wScr, hScr = pyautogui.size()
print(hScr, wScr)

while True:
    # 1. gambar dan menemukan hand landmark
    seccess, img = cap.read()
    # start = time.time()
    # sum = 0
    # N = 100
    # for i in range(0, N):
    #     for j in range(0, N):
    #         sum += 1
    # end = time.time()
    # second = end - start
    # fps = smoothing / second
    Hands, img = detector.findHands(img, flipType=False)
    # cek function hand lancmark
    # if len(Hands):
    #     hand1 = Hands[0]
    #     lmList1 = hand1["lmList"]  # list dari 21 landmark point
    #     bbox1 = hand1["bbox"]  # info dari index box x,y,w,h
    #     centerPoint1 = hand1["center"]  # titik tengah dari tangan cx, cy
    #     handType = hand1["type"]  # cek tangan right or left
    #     finger1 = detector.fingersUp(hand1)

    #     # print(len(lmList1), lmList1)
    #     # print(handType)
    #     # print(bbox1)
    #     # print(centerPoint1)
    # if len(Hands) == 2:
    #     hand2 = Hands[1]  # list dari 21 landmark
    #     lmList2 = hand2["lmList"]
    #     bbox2 = hand2["bbox"]  # info dari index box x,y,w,h
    #     centerPoint2 = hand2["center"]  # titik tengah dari tangan cx, cy
    #     handType2 = hand2["type"]  # cek tangan right or left
    #     finger2 = detector.fingersUp(hand2)

    #     print(finger1, finger2)
    #     # print(handType2, handType)

    # 2. dapatkan ttitk dari dari jari telunjuk dan jempol
    if len(Hands):
        hand1 = Hands[0]
        fingers = detector.fingersUp(hand1)
        lmList = hand1["lmList"]
        x0, y0 = lmList[4][0], lmList[4][1]
        x1, y1 = lmList[8][0], lmList[8][1]
        x2, y2 = lmList[4][0], lmList[4][1]
        x3, y3 = lmList[12][0], lmList[12][1]
        x4, y4 = lmList[16][0], lmList[16][1]
        # print(x1, y1, x2, y2)
        # 3. cek apakah jari mengangkat
        print(fingers)
        # 4. semua jari terangkat : Moving Mode
        if fingers[3] == 0 and fingers[4] == 0:
            # 5. convert coordinate
            cv2.rectangle(img, (frameR, frameR),
                          (wCam-frameR, hCam-frameR), (0, 0, 255), 2)
            x5 = np.interp(x3, (frameR, wCam - frameR), (0, wScr))
            y5 = np.interp(y3, (frameR, hCam - frameR), (0, hScr))
            # print(y3, x3)
            # 6. perhalus nilai supaya mudah di proses
            clocX = plocX + (x5 - plocX) / smoothing
            clocY = plocY + (y5 - plocY) / smoothing

            # 7. Move mouse
            mouse.move(wScr - clocX, clocY)

            cv2.circle(img, (x3, y3), 15, (255, 0, 0), cv2.FILLED)
            plocX, plocY = clocX, clocY
    # 8. menjalankan function : Click Mode
        lenght = math.hypot(x0 - x1, y0 - y1)
        # print(lenght)
        # 9. menemukan jarak antara jari
        if lenght < 20:
            # jika jarak antar telunjuk dan jempol menekuk : clock kiri
            cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
            mouse.click()
            # print(lenght)
         # jika jari tengan dan jari manis berdekatan maka : right click mode
        if fingers[2] == 1 and fingers[3] == 1:
            # menemkan jarak antar jari tengan dan jari manis
            lenght = math.hypot(x3-x4, y3-y4)
            # print(lenght)
            # click kanan
            if lenght < 30:
                cv2.circle(img, (x4, y4), 15, (0, 0, 255), cv2.FILLED)
                mouse.right_click()
                print(lenght)

            if len(Hands) == 2:
                hand2 = Hands[1]
                tengah = hand2["lmList"]
                xx2, yy2 = tengah[12][0], tengah[12][1]
                lenght, info, img = detector.findDistance(
                    (xx2, yy2), (x3, y3), img)
                if lenght != 0:
                    scale = int((lenght - xx2) // 2)
                    print(scale)
                    pyautogui.scroll(scale)

            # 11. frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Display
    cv2.imshow("Virtual Mouse", img)
    cv2.waitKey(1)
