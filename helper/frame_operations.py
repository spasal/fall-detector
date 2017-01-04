import numpy as np
import cv2

_useGaussian = True
_gaussianPixels = 21

def prepare_frame(frame):
    """
    todo
    """
    # frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if _useGaussian: gray = cv2.GaussianBlur(gray, (_gaussianPixels, _gaussianPixels), 0)
    return frame, gray


def find_largest_contour(binary_threshold):
    (img, contours, hierarchy) = cv2.findContours(
        binary_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_area = 0
    largest_contour = contours[0] if len(contours) > 0 else None

    for cnt in contours:
        if len(cnt) < 6:
            continue

        if cv2.contourArea(cnt) < 2000:
            continue

        if cv2.contourArea(cnt) > largest_area:
            largest_area = cv2.contourArea(cnt)
            largest_contour = cnt

    if largest_contour is not None:
        largest_contour = largest_contour if len(largest_contour) > 6 else None
    return largest_contour


def clean_frame_within_contour(src, contour):
    """
    todo
    """
    mask = np.zeros_like(src)
    ellipse = cv2.fitEllipse(contour)
    mask = cv2.ellipse(mask, ellipse, (255, 255, 255), -1)
    src = np.bitwise_and(src, mask)
    return src


'''' DRAWING FUNCTIONS '''
__font_face, __font_scale, = cv2.FONT_HERSHEY_SIMPLEX, 0.75
__font_color, __font_thickness = (255, 255, 255), 2
__min_width, __min_height = 0, 0
__max_width, __max_height = 0, 0

def draw_ellipse(frame, contour, is_fall=False):
    ellipse = cv2.fitEllipse(contour)
    color = (0, 0, 255) if is_fall is True else (0, 255, 0)
    cv2.ellipse(frame, ellipse, color, 2)

def draw_feature_extraction(vector_angles, delta_angle, movement, src):
    angle1, org1 = "primary PCA: " + str(int(vector_angles[0])), (__min_width + 10, __min_height + 30)
    angle2, org2 = "secondary PCA: " + str(int(vector_angles[1])), (__min_width + 10, __min_height + 60)
    angle3, org3 = "PCA delta: " + str(int(delta_angle)), (__min_width + 10, __min_height + 90)
    movement, org4 = "movement: " + str(movement), (__min_width + 10, __min_height + 120)

    cv2.putText(src, angle1, org1, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, angle2, org2, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, angle3, org3, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, movement, org4, __font_face, __font_scale, __font_color, __font_thickness)
