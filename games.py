import mediapipe as mp
import cv2
import numpy as np
import pyautogui

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Pose
pose = mp.solutions.pose.Pose()
drawing = mp.solutions.drawing_utils

space_down = False
w_down = False

while True:
    # Capture frame-by-frame
    ret, frm = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Convert the frame to RGB
    res = pose.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    # Draw landmarks
    if res.pose_landmarks:
        drawing.draw_landmarks(frm, res.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        # Check for kick punch combination
        if res.pose_landmarks.landmark[16].visibility > 0.7:
            x = abs(res.pose_landmarks.landmark[16].x * 640 - res.pose_landmarks.landmark[12].x * 640)
            if x > 90:
                print('kick punch combination detected')
                if not space_down:
                    for _ in range(3):
                        pyautogui.press('space')
                    space_down = True
                else:
                    pyautogui.keyUp('space')
                    space_down = False

        # Check for special attack move
        if res.pose_landmarks.landmark[16].y * 640 < res.pose_landmarks.landmark[10].y:
            print('special attack move')
            if not w_down:
                pyautogui.keyDown('w')
                w_down = True
            else:
                pyautogui.keyUp('w')
                w_down = False

    # Flip the frame horizontally for a selfie-view display
    frm = cv2.flip(frm, 1)

    # Display the resulting frame
    cv2.imshow('window', frm)

    # Break the loop on 'ESC' key press
    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything is done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
