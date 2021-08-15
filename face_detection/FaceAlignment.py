import cv2
import dlib
import numpy as np
from time import time
from util.constant import SHAPE_PREDICTOR_PATH



LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]


def rect_to_tuple(rect):
    left = rect.left()
    right = rect.right()
    top = rect.top()
    bottom = rect.bottom()
    return left, top, right, bottom


def extract_eye(shape, eye_indices):
    points = map(lambda i: shape.part(i), eye_indices)
    return list(points)


def extract_eye_center(shape, eye_indices):
    points = extract_eye(shape, eye_indices)
    xs = map(lambda p: p.x, points)
    ys = map(lambda p: p.y, points)
    return sum(xs) // 6, sum(ys) // 6


def extract_left_eye_center(shape):
    return extract_eye_center(shape, LEFT_EYE_INDICES)


def extract_right_eye_center(shape):
    return extract_eye_center(shape, RIGHT_EYE_INDICES)


def angle_between_2_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    tan = (y2 - y1) / (x2 - x1)
    return np.degrees(np.arctan(tan))


def get_rotation_matrix(p1, p2):
    angle = angle_between_2_points(p1, p2)
    x1, y1 = p1
    x2, y2 = p2
    xc = (x1 + x2) // 2
    yc = (y1 + y2) // 2
    M = cv2.getRotationMatrix2D((xc, yc), angle, 1)
    return M


def crop_image(image, det):
    left, top, right, bottom = rect_to_tuple(det)
    return image[max(top, 0):min(bottom, image.shape[0]), max(left, 0):min(right, image.shape[1])]


def faceAlignmentAndCropping(input_img):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
    if input_img.ndim == 3:
        img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    else:
        img = input_img
    width, height = img.shape[:2]
    # dets = extract_face(img)
    start = time()
    dets = detector(img, 1)
    print("detection took: {}".format(time() - start))
    img = input_img
    cropped_array = []

    for i, det in enumerate(dets):
        cropped = crop_image(img, det)
        cropped_array.append(cropped)

    return cropped_array, dets
