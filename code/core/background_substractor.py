_initialized = False
def init():
    global _initialized
    if not _initialized:
        import cv2
        _backgroundSubstractor = cv2.createBackgroundSubtractorMOG2()
        _threshholdLimit = 35
        _dilationIterations = 25
        _initialized = True

import cv2
_backgroundSubstractor = cv2.createBackgroundSubtractorMOG2()
_threshholdLimit = 35
_dilationIterations = 25

def background_substraction(frame):
    """
    Frame should be blurred and converted to gray
    Returns MOG2_Mask and binaryThreshold after dilation
    """
    init()
    backgroundMask = _backgroundSubstractor.apply(frame)
    

    binTreshold = cv2.threshold(
        backgroundMask, _threshholdLimit, 255, cv2.THRESH_BINARY
    )[1]
    binTreshold = cv2.dilate(binTreshold, None, iterations=_dilationIterations)
    return backgroundMask, binTreshold