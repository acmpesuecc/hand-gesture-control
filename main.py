import numpy as np
import mediapipe as mp
import cv2
import time
import threading
import hand_position

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not detected. Exiting.")
    exit()

def hand_tracking():
    with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.4,
        min_tracking_confidence=0.4) as hands:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Error: Unable to read frame. Exiting.")
                break

            h, w, c = image.shape
            start = time.perf_counter()

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            image.flags.writeable = False

            results = hands.process(image)

            image.flags.writeable = True

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if hand_landmarks.landmark:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                                  mp_drawing_styles.get_default_hand_landmarks_style(),
                                                  mp_drawing_styles.get_default_hand_connections_style())

                        index_finger_tip = hand_landmarks.landmark[0]

                        index_finger_tip_x = index_finger_tip.x * w
                        index_finger_tip_y = index_finger_tip.y * h

                        if index_finger_tip_x > w/2:
                            cv2.putText(image, "Right", (500, 70),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 250))
                        elif index_finger_tip_x < w/2:
                            cv2.putText(image, "Left", (500, 70),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (250, 0))

                cv2.line(image, (int(w/2), 0), (int(w/2), h), (0, 255, 0), 2)

                end = time.perf_counter()
                totalTime = end - start

                fps = 1/totalTime

                cv2.putText(image, f'FPS: {int(fps)}', (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
                cv2.imshow('MediaPipe Hands', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

key_stimulation_thread = threading.Thread(target=hand_position.stimulate_keys)

key_stimulation_thread.start()

hand_tracking()