import cv2
import mediapipe
import pyautogui
from math import hypot
import numpy as np


mp_hands = mediapipe.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_trackging_confidence=0.5)
mp_draw = mediapipe.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    OK, frame = cap.read()

    if not OK: continue

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmark.landmark):
                h,w,c = frame.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
            if lm_list:
                x1,y1, = lm_list[4][1], lm_list[4][2] # Thumb
                x2,y2 = lm_list[8][1], lm_list[8][2] # Index 
                cv2.circle(frame, (x1,y1), 10, (255,0,255), cv2.FILLED)
                cv2.circle(frame, (x2,y2), 10, (255,0,255), cv2.FILLED)
                
                length = hypot(x2 - x1, y2 - y1)
                vol_per = np.interp(length, [20,200], [0,100])
                vol_per = np.clip(vol_per, 0, 100)

                if length < 30:
                    pyautogui.press("volumemute")
                elif length > 70:
                    pyautogui.press("volumeup")
                else:
                    pyautogui.press("volumedown")

                cv2.putText(frame, f"Volume: {int(vol_per)}%", (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
            
    cv2.imshow("Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

                