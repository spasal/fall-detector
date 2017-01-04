''''
Motion History Image (MHI) is used to calculate the movement coefficient. 
It shows recent motion in the image.
'''
import imutils
import numpy as np
import sys
import cv2

__this = sys.modules[__name__]
__this.is_initialized = False

__this.mhi_duration = None
__this.min_time_delta, __this.max_time_delta = None, None
__this.motion_history = None
__this.hsv = None
__this.timestamp = None
__this.prev_frame = None

def initialze_mhi(first_frame):
    if __this.is_initialized is False:
        # frame = imutils.resize(first_frame, width=500)
        frame = first_frame
        h, w = frame.shape[:2]

        __this.mhi_duration = 10 # 0.5 # 
        __this.min_time_delta, __this.max_time_delta = 0.05, 0.25
        __this.motion_history = np.zeros((h, w), np.float32)
        __this.hsv = np.zeros((h, w, 3), np.uint8)
        __this.hsv[:,:,1] = 255
        __this.timestamp = 0
        __this.prev_frame = frame.copy()

        __this.is_initialized = True
    else:
        msg = "MHI is already initialized."
        raise RuntimeError(msg)


def calculate_mhi_frame(fgmask, frame):
    # 1 calculate & normalize new mhi frame
    cv2.motempl.updateMotionHistory(fgmask, __this.motion_history, __this.timestamp, __this.mhi_duration)
    mhi = np.uint8(np.clip((__this.motion_history-(__this.timestamp-__this.mhi_duration)) / __this.mhi_duration, 0, 1)*255)
    
    __this.prev_frame = frame.copy()
    __this.timestamp += 1
    
    return mhi

def calculate_movement_coeff(contour, current_frame, previous_frame, test=False):
    current = current_frame.copy()

    if __check_if_frame_is_not_white(previous_frame):
        difference = cv2.absdiff(current_frame, previous_frame)
        sum_difference = sum(sum(difference))
        cnt_area = cv2.contourArea(contour)
        frm_area = current_frame.shape[0] * current_frame.shape[1]
        # print(sum_difference, ' * ', cnt_area, ' / ', frm_area)
        normalised = (sum_difference * cnt_area) / (frm_area * 1000)
        textName = "test motion coeff " + str(test)
        cv2.imshow(textName, difference)
        return round(normalised, 3)
    else:
        return 0

def __check_if_frame_is_not_white(frame):
    return False if sum(sum(frame % 255)) == 0 else True