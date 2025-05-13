import os
import cv2
import face_recognition
import numpy as np

def detected(imgblob):
    arr = np.frombuffer(imgblob, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face = face_recognition.face_encodings(rgbImg)

    if len(face) == 0:
        return False
    else:
        return True


def compare(img1blob, img2blob):
    arr1 = np.frombuffer(img2blob, np.uint8)
    arr2 = np.frombuffer(img2blob, np.uint8)
    img1 = cv2.imdecode(arr1, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(arr2, cv2.IMREAD_COLOR)
    rgbImg1 = cv2.cvtColor(img1, cv2.COLOR_RGBA2RGB)
    rgbImg2 = cv2.cvtColor(img2, cv2.COLOR_RGBA2RGB)
    faces1 = face_recognition.face_encodings(rgbImg1)
    faces2 = face_recognition.face_encodings(rgbImg2)

    if faces1 is None or faces2 is None or len(faces1) == 0 or len(faces2) == 0:
        return -1
    else:
        res = face_recognition.compare_faces([faces1[0]], faces2[0])
        if res[0] == True:
            return 1
        else:
            return 0