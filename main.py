import cv2
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import mediapipe as mp
import math
import HandTrackingModule as htm
import numpy as np


mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.75)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)


minVol, maxVol, _ = volume.GetVolumeRange()

while True:
    suc, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)

        # 25 to 130
        # -65 to 0

        vol = np.interp(length, [25,150], [minVol, maxVol])
        volBar = np.interp(length, [25, 150], [400, 150])
        volPer = np.interp(length, [25, 150], [0, 100])

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 255))
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 255), cv2.FILLED)

        cv2.putText(img, f'{int(volPer)} %', (50, 450   ), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)

        if (length < 25):
            cv2.circle(img, (cx, cy), 7, (255, 255, 0), cv2.FILLED)

        volume.SetMasterVolumeLevel(vol, None)




    cv2.imshow("output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
