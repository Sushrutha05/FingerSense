import cv2
import mediapipe as mp
from collections import deque

VOTE_WIN = 10
VOTE_NEED = 3
gesture_history = deque(maxlen = VOTE_WIN)

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

middle_confirmed = False

with mp_hands.Hands(
    model_complexity = 1,
    min_detection_confidence = 0.3,
    min_tracking_confidence = 0.3) as hands:

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print("Failed to grab frame")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
    
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            
            landmarks = hand_landmarks.landmark
            img_h, img_w , _= frame.shape

            wrist_y = landmarks[0].y

            tips_y = [landmarks[i].y for i in [8,12,16,20]]
            top_tip_y = min(tips_y)
            hand_height = wrist_y - top_tip_y

            finger_flags = []
            for tip_i, pip_i in zip([4,8,12,16,20], [2,5,9,13,17]):
                tip_rel = wrist_y - landmarks[tip_i].y
                norm_height = tip_rel / hand_height if hand_height else 0
                is_up = 1 if norm_height > 0.6 else 0
                finger_flags.append(is_up)

            is_middle = (finger_flags == [0,0,1,0,0])
            gesture_history.append(is_middle)
            middle_confirmed = sum(gesture_history) >= VOTE_NEED
        else:
            gesture_history.clear()
            middle_confirmed = False

        if middle_confirmed:
            try:
                xs = [int(landmarks[i].x * img_w) for i in [9,10,11,12]]
                ys = [int(landmarks[i].y * img_h) for i in [9,10,11,12]]

                x1, x2 = max(min(xs) - 20, 0), min(max(xs) + 20, img_w)
                y1, y2 = max(min(ys) - 20, 0), min(max(ys) + 20, img_h)

                pad = 5
                x1_p = max(x1 - pad, 0)
                x2_p = min(x2 + pad, img_w)
                y1_p = max(y1 - pad, 0)
                y2_p = min(y2 + pad, img_h)

                roi = frame[y1_p:y2_p, x1_p:x2_p]
                if roi.size > 0:
                    blur = cv2.GaussianBlur(roi, (99, 99), 0)
                    frame[y1_p:y2_p, x1_p:x2_p]= blur
                    cv2.putText(frame, "Middle Finger Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            except Exception as e:
                print(f"Skipping blur due to error: {e}")
        else:
            cv2.putText(frame, " ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
        cv2.imshow('webcam', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()