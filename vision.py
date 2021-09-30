import cv2 as ocv
import mediapipe as mp
import numpy as np
from math import acos, degrees

from mediapipe.python.solutions import pose

# TRANSFORMAR EN CLASE
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
height = None
width = None
result = None

up = False
down = False
count = 0


def process_frame(frame):
    global height, width, result

    with mp_pose.Pose(static_image_mode=False, min_tracking_confidence=0.5, min_detection_confidence=0.5) as pose:
        height, width, _ = frame.shape

        frame.flags.writeable = False
        result = pose.process(frame)
        frame.flags.writeable = True

        if result.pose_landmarks is not None:
            # Puntos de la cadera
            p1 = find_landmarks(24)

            # Puntos de la rodilla
            p2 = find_landmarks(26)

            # Puntos del tobillo
            p3 = find_landmarks(28)

            angle = calc_angle(p1, p2, p3)

            is_squat(angle)

            frame = draw_frame(p1, p2, p3, frame, angle)

    return frame


def find_landmarks(i):
    x = int(result.pose_landmarks.landmark[i].x * width)
    y = int(result.pose_landmarks.landmark[i].y * height)

    return np.array([x, y])


def calc_angle(p1, p2, p3):
    # Se calculan sus 3 lados
    l1 = np.linalg.norm(p2 - p3)
    l2 = np.linalg.norm(p1 - p3)
    l3 = np.linalg.norm(p1 - p2)

    # Se calcula el angulo
    return degrees(acos((l1 ** 2 + l3 ** 2 - l2 ** 2) / (2 * l1 * l3)))


def is_squat(angle):
    global up, down, count

    if angle >= 160:
        up = True

    if up and not down and angle <= 70:
        down = True

    if up and down and angle >= 160:
        count += 1
        up = False
        down = False


def draw_frame(p1, p2, p3, frame, angle):
    # Imagen auxiliar con solo las lineas
    aux_image = np.zeros(frame.shape, np.uint8)

    ocv.line(aux_image, (p1[0], p1[1]), (p2[0], p2[1]), (255, 255, 0), 20)
    ocv.line(aux_image, (p2[0], p2[1]), (p3[0], p3[1]), (255, 255, 0), 20)
    ocv.line(aux_image, (p1[0], p1[1]), (p3[0], p3[1]), (255, 255, 0), 5)

    # Contorno
    contours = np.array([p1, p2, p3])
    ocv.fillPoly(aux_image, pts=[contours], color=(128, 0, 250))

    output = ocv.addWeighted(frame, 1, aux_image, 0.8, 0)

    # Se pintan los puntos
    ocv.circle(output, (p1[0], p1[1]), 6, (0, 255, 255), 4)
    ocv.circle(output, (p2[0], p2[1]), 6, (128, 0, 250), 4)
    ocv.circle(output, (p3[0], p3[1]), 6, (255, 191, 0), 4)

    # Se imprime el angulo
    ocv.putText(output, str(int(angle)), (p2[0] + 30, p2[1]), 1, 1.5, (128, 0, 250), 2)

    # Se muestra el contador de sentadillas
    # ocv.rectangle(output, (0, 0), (85, 60), (98, 174, 30), -1)
    # ocv.putText(output, str(count), (10, 50), 1, 3.5, (255, 255, 255), 2)

    # Imagen axuiliar
    return output
