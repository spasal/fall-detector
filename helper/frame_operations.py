import numpy as np
import cv2

'''' FRAME PREPARATION AND CLEANUP '''
_min_Area = 100*100
_useGaussian = True
_gaussianPixels = 21

def prepare_frame(frame):
    """
    todo
    """

    ''''
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    frame = imutils.resize(frame, width=500)
    '''
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if _useGaussian:
        gray = cv2.GaussianBlur(gray, (_gaussianPixels, _gaussianPixels), 0)
    return frame, gray


def find_largest_contour(binary_threshold):
    (img, contours, hierarchy) = cv2.findContours(
        binary_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_area = 0
    largest_contour = contours[0] if len(contours) > 0 else None

    for cnt in contours:
        if len(cnt) < 6:
            continue
        
        if cv2.contourArea(cnt) < _min_Area:
            continue

        if cv2.contourArea(cnt) > largest_area:
            largest_area = cv2.contourArea(cnt)
            largest_contour = cnt

    if largest_contour is not None:
        if len(largest_contour) < 6 or cv2.contourArea(largest_contour) < _min_Area:
            largest_contour = None

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
__font_face, __font_scale, = cv2.FONT_HERSHEY_SIMPLEX, 1.25
__font_color, __font_thickness = (255, 255, 255), 3
__min_width, __min_height = 0, 0
__max_width, __max_height = 0, 0
__base_val = 40

def draw_ellipse(frame, contour, color_code, is_fall=False):
    ellipse = cv2.fitEllipse(contour)
    cv2.ellipse(frame, ellipse, color_code, 2)

def draw_rectangle(frame, contour, is_fall=False):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    color = (0, 0, 255) if is_fall is True else (0, 255, 0)
    cv2.drawContours(frame, [box], 0, color, 2)

def draw_feature_extraction(vector_angles, delta_angle, movement, src):
    angle1, org1 = "primary PCA: " + str(int(vector_angles[0])), (__min_width + 10, __min_height + 1 * __base_val)
    angle2, org2 = "secondary PCA: " + str(int(vector_angles[1])), (__min_width + 10, __min_height + 2 * __base_val)
    angle3, org3 = "PCA delta: " + str(int(delta_angle)), (__min_width + 10, __min_height + 3 * __base_val)
    movement, org4 = "movement: " + str(movement), (__min_width + 10, __min_height + 4 * __base_val)

    cv2.putText(src, angle1, org1, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, angle2, org2, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, angle3, org3, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, movement, org4, __font_face, __font_scale, __font_color, __font_thickness)

    if __max_width == 0 or __max_height == 0:
        print(type(src))
        print(src.shape)
        global __max_width, __max_height
        __max_width = src.shape[1]
        __max_height = src.shape[0]


import sys
__delta = ""
# print(sys.getdefaultencoding())
# print(u"\N{GREEK CAPITAL LETTER DELTA}")

def draw_fall_detection(mean_direction_diff_vec, mean_delta_pca, mean_angle_pcas, color_code, src):
    # mean_direction_diff_vec
    mean_dir_diff_vec_x, mean_dir_diff_vec_y = (
        int(mean_direction_diff_vec[0]), int(mean_direction_diff_vec[1]))
    mean_dir_diff_vec_txt, org1 = __delta + "Mean Vector: %s | %s" % (
        mean_dir_diff_vec_x, mean_dir_diff_vec_y), (__min_width + 10, __max_height - 1 * __base_val)
    
    # mean_pca_angles
    mean_angle_pcas_x, mean_angle_pcas_y = (
        int(mean_angle_pcas[0]), int(mean_angle_pcas[1]))
    mean_angle_pcas_txt, org3 = __delta + "Mean PCA Angles: %s | %s" % (
        mean_angle_pcas_x, mean_angle_pcas_y), (__min_width + 10, __max_height - 2 * __base_val)
    
    # mean_pca_delta
    mean_delta_pca = int(mean_delta_pca)
    mean_delta_pca, org2 = "Median PCA Delta: %s" % (
        mean_delta_pca), (__min_width + 10, __max_height - 3 * __base_val)

    cv2.putText(src, mean_dir_diff_vec_txt, org1, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, mean_angle_pcas_txt, org3, __font_face, __font_scale, __font_color, __font_thickness)
    cv2.putText(src, mean_delta_pca, org2, __font_face, __font_scale, __font_color, __font_thickness)

    if color_code != (0, 255, 0):
        text = "COLOR NOT DEFINED"
        print(color_code)
        if color_code == (0, 255, 255):
            text = "FALL SIMPLE"
        elif color_code == (0, 165, 255):
            text = "FALL ADVANCED"
        elif color_code == (0, 0, 255):
            text = "!IS FALL!"
        
        org = (int(__max_width / 2) - 100, int(__max_height / 2))

        cv2.putText(src, text, org, __font_face, __font_scale, __font_color, __font_thickness)

