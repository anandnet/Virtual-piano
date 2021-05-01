from mediapipe.python import solutions
import cv2
import numpy as np
mp_drawing = solutions.drawing_utils
mp_hands = solutions.hands
circle_spec = mp_drawing.DrawingSpec(color=(0, 255, 255), circle_radius=0)
connection_spec = mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=8)

# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7)


def detect_hand(frame):
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    blank_image = np.zeros((image.shape[0],image.shape[1],3), np.uint8)
    right_hand_status, left_hand_status = None, None
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if results.multi_handedness[i].classification[0].label == "Right":
                right_hand_status = get_finger_status(hand_landmarks.landmark,1)
                

            if results.multi_handedness[i].classification[0].label == "Left":
                left_hand_status = get_finger_status(hand_landmarks.landmark,0)
            mp_drawing.draw_landmarks(blank_image, hand_landmarks,landmark_drawing_spec=circle_spec,connection_drawing_spec=connection_spec,connections=mp_hands.HAND_CONNECTIONS)

    
    return left_hand_status,right_hand_status,blank_image



def get_finger_status(landmark,hnd_index):
    if(hnd_index==0):
        thumb = is_fingure_close(landmark[4].x, landmark[3].x, landmark[2].x)
    else:
        thumb = is_fingure_close(landmark[2].x, landmark[3].x, landmark[4].x)

    index = is_fingure_close(landmark[6].y, landmark[7].y, landmark[8].y)
    middle = is_fingure_close(landmark[10].y, landmark[11].y, landmark[12].y)
    ring = is_fingure_close(landmark[14].y, landmark[15].y, landmark[16].y)
    little = is_fingure_close(landmark[18].y, landmark[19].y, landmark[20].y)
    palm_up = not thumb and not index and not middle and not ring and not little
    #palm_dowm = thumb and index and middle and ring and little
    return [palm_up, thumb, index, middle, ring, little]


def is_fingure_close(fixkeypoint, point1, point2):
    return point1 > fixkeypoint and point2 > fixkeypoint
