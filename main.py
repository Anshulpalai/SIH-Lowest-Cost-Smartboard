import cv2
import mouse
import numpy as np
import HandTrackingModule as htm
import time
import autopy
# import pyautogui

#################################
wCam, hCam = 640, 480
frameR = 200  # Frame Reduction
smoothening = 10
#################################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img1 = cap.read()
    img1 = detector.findHands(img1)
    lmList, bbox = detector.findPosition(img1)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # fx3, fy3 = lmList[16][1:]
        # fx4, fy4 = lmList[20][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        cv2.rectangle(img1, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img1, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            # 9. Find distance between fingers
            length, img1, lineInfo = detector.findDistance(4, 8, 12, 16, 20, img1)
            # print(length)
            # 10. Click mouse if distance short
            if length < 180:
                cv2.circle(img1, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                # cv2.flip(img1, 1)
                mouse.click()
        # 9. If Index, middle and Ring Fingers are up: Scroll Up
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            # 9. Find distance between fingers
            length, img1, lineInfo = detector.findDistance(4, 8, 12, 16, 20, img1)
            # print(length)
            # 10. Click mouse if distance short
            if length < 180:
                cv2.circle(img1, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                mouse.wheel(1)
        # 10. If index, middle, ring and pinky fingers are up: Scroll Down
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            # 9. Find distance between fingers
            length, img1, lineInfo = detector.findDistance(4, 8, 12, 16, 20, img1)
            # print(length)
            # 11. Click mouse if distance short
            if length < 180:
                cv2.circle(img1, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                mouse.wheel(-1)

        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
            length, img1, lineInfo = detector.findDistance(4, 8, 12, 16, 20, img1)
            # print(length)
            # 11. Click mouse if distance short
            if length < 180:
                cv2.circle(img1, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
            # pyautogui.hotkey('alt', 'tab')
                mouse.press()

        # if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
        #     length, img1, lineInfo = detector.findDistance(4, 8, 12, 16, 20, img1)
        #     print(length)
        #     # 11. Click mouse if distance short
        #     if length > 40:
        #         cv2.circle(img1, (lineInfo[4], lineInfo[5]),
        #                    15, (0, 255, 0), cv2.FILLED)
        #         pyautogui.screenshot()

    # 12. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img1, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 255), 3)
    # 13. Display
    cv2.imshow("Image", img1)
    cv2.waitKey(10)
