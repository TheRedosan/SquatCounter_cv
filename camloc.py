import cv2 as ocv


def camera_list():
    index = 0
    arr = []
    i = 10

    while i > 0:
        cap = ocv.VideoCapture(index, ocv.CAP_DSHOW)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1

    return arr
