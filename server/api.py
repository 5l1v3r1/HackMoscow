import os

import dlib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(os.path.join(os.path.join(BASE_DIR, 'server'),'shape_predictor_5_face_landmarks.dat'))
facerec = dlib.face_recognition_model_v1(os.path.join(os.path.join(BASE_DIR, 'server'),'dlib_face_recognition_resnet_model_v1.dat'))
savedDescriptors = []

def mncalc(t1, t2):
    try:
        return 1 - (np.dot(t1, t2) / (np.sqrt(np.dot(t1, t1)) * np.sqrt(np.dot(t2, t2))))
    except:
        return 100


def find(desc, data):
    for i in data:
        z = mncalc(desc, i)
        if z < 0.06:
            return True
    return False

def extract_descriptor(img):
    try:
        face_face = []
        dets_webcam = detector(img, 1)
        for k, d in enumerate(dets_webcam):
            shape = sp(img, d)
            face_face.append(facerec.compute_face_descriptor(img, shape))
        return face_face
    except RuntimeError:
        print('error')


def check_people(img):
    test_face = extract_descriptor(img)
    for face in test_face:
        ans = find(face, savedDescriptors)
        if ans == False:
            savedDescriptors.append(face)
    if savedDescriptors:
        return len(savedDescriptors)
    else:
        return 0


