import cv2
import pygame
import mediapipe as mp
import math
from config import *

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

current_cursor_x = 0.5
current_cursor_y = 0.5

clamp = min(WINDOW_WIDTH, WINDOW_HEIGHT) / 2

def body_cursor():
    global current_cursor_x, current_cursor_y
    success, img = cap.read()
    if not success:
        return

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)
    target_x = current_cursor_x
    target_y = current_cursor_y

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[8]
            target_x = index_finger_tip.x
            target_y = index_finger_tip.y
    else:
        target_x = 0.5
        target_y = 0.5

    current_cursor_x += (target_x - current_cursor_x) * SMOOTHING_FACTOR
    current_cursor_y += (target_y - current_cursor_y) * SMOOTHING_FACTOR

    current_cursor_x = max(0, min(clamp, current_cursor_x))
    current_cursor_y = max(0, min(clamp, current_cursor_y))

    return current_cursor_x - 0.5, current_cursor_y - 0.5

# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_gesture(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    if f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50: # 0
        return True
    else:
        return False        

def gesture_detection():
    sucess, img = cap.read()
    if not sucess:
        return False
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)                # 偵測手勢

    dt = CLOCK.tick(FPS) / 1000

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            finger_points = []                   # 記錄手指節點座標的串列
            for i in hand_landmarks.landmark:
                # 將 21 個節點換算成座標，記錄到 finger_points
                x = i.x*WINDOW_WIDTH
                y = i.y*WINDOW_HEIGHT
                finger_points.append((x,y))
            if finger_points:
                finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                # 根據手指角度，判斷手勢      
                if hand_gesture(finger_angle):

                    return True
                else:
                    return False

