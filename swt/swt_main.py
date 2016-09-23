"""
Module to run the SWT on a given image
"""

import os
import sys
import getopt
import cv2 as cv
import numpy as np
from swt import swt_detect_text
from swt import swt_connected_components

if __name__ == "__main__":
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], 'i:b:')
    except getopt.GetoptError:
        print 'Usage: python swt_main.py -i <input_file> -b <background>'
        sys.exit(2)

    IMAGE_PATH = str()
    BACKGROUND = bool(False)
    for opt, arg in OPTS:
        if opt == '-i':
            IMAGE_PATH = arg
        elif opt == '-b':
            if arg == '1':
                BACKGROUND = True

    if os.path.isfile(IMAGE_PATH):
        pass
    else:
        print 'Error: Image file does not exist!'
        sys.exit(2)

    IMG = cv.imread(IMAGE_PATH, 0)
    DETECT_TEXT = swt_detect_text.StrokeWidthTransform(IMG, BACKGROUND)
    DETECT_TEXT.execute_swt()
    CONN_COMPONENTS = swt_connected_components.ConnectedComponents(DETECT_TEXT.swt_image)
    CONN_COMPONENTS.find_connected_components()

    print len(np.unique(CONN_COMPONENTS.dsa))
