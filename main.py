import cv2
import numpy as np
import serial
import time
from cvzone.HandTrackingModule import HandDetector


detector = HandDetector(detectionCon=0.7, maxHands=1)

transmitter = serial.Serial('COM3', 115200)
time.sleep(2)

def send_servo_command(pan_or_tilt, angle):
    servo_num = 1 if pan_or_tilt == 'pan' else 2
    angle = max(0, min(angle, 180))
    coordinates = f"{servo_num},{angle}\r"
    transmitter.write(coordinates.encode())
    print(f"Sent command: {pan_or_tilt} to {angle} degrees")


def detect_laser_point(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([160, 100, 100])
    upper_red = np.array([179, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask1 + mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        if radius > 3:
            cv2.circle(frame, center, int(radius), (0, 255, 0), 2)
            return center

    return None


def track_laser_and_hand():
    pan_angle = 90
    tilt_angle = 90  
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera could not be opened.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        hands, img = detector.findHands(frame, flipType=False)
        hand_center = None

        if hands:
            lmList = hands[0]['lmList']
            x, y = lmList[9][:2] 
            hand_center = (x, y)
            cv2.circle(img, hand_center, 10, (255, 0, 0), -1)
            print(f"Hand Center: X={hand_center[0]}, Y={hand_center[1]}")


        laser_position = detect_laser_point(img)
        if laser_position:
            print(f"Laser Position: X={laser_position[0]}, Y={laser_position[1]}")
            cv2.circle(img, laser_position, 5, (0, 255, 0), -1)


        if hand_center and laser_position:
            delta_x = hand_center[0] - laser_position[0]
            delta_y = hand_center[1] - laser_position[1]

            if abs(delta_x) > 10:
                pan_angle -= 1 if delta_x > 0 else -1
                send_servo_command('pan', pan_angle)

            if abs(delta_y) > 10:
                tilt_angle += 1 if delta_y > 0 else -1
                send_servo_command('tilt', tilt_angle)

        cv2.imshow('Laser and Hand Tracker', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

track_laser_and_hand()
