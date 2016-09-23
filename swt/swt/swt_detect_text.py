"""
Module containing the implementation of the SWT Algorithm
"""

import math
import cv2 as cv
import numpy as np
from . import swt_connected_components

class StrokeWidthTransform(object):
    """
    Class implementing the main SWT Algorithm
    """

    def __init__(self, input_image, background):
        self.input_image = input_image
        self.image_shape = self.input_image.shape
        self.background = background

        self.swt_image = np.empty(self.image_shape)
        self.swt_image[:] = np.Infinity
        self.rays = []

        self.canny_image = np.zeros(self.image_shape, np.uint8)
        self.gauss_image = np.zeros(self.image_shape, np.float64)
        self.gradx_image = np.zeros(self.image_shape, np.float64)
        self.grady_image = np.zeros(self.image_shape, np.float64)
        self.theta_image = np.zeros(self.image_shape, np.float64)

    def initialize_images(self):
        """
        Method to initialize the Canny, Gaussian and Gradient Images
        """

        self.canny_image = cv.Canny(self.input_image, 175, 320, apertureSize=3)

        self.gauss_image = self.input_image * (1.0/255.0)
        self.gauss_image = cv.GaussianBlur(self.gauss_image, (5, 5), 0)

        self.gradx_image = cv.Sobel(self.gauss_image, -1, 1, 0, ksize=-1)
        self.grady_image = cv.Sobel(self.gauss_image, -1, 0, 1, ksize=-1)
        self.theta_image = np.arctan2(self.gradx_image, self.grady_image)

        self.gradx_image = cv.GaussianBlur(self.gradx_image, (3, 3), 0)
        self.grady_image = cv.GaussianBlur(self.grady_image, (3, 3), 0)

    def visualize_images(self):
        """
        Method to display the Images
        """

        while cv.waitKey(30) != 27:
            cv.imshow('Original Image', self.input_image)
            cv.imshow('Canny Image', self.canny_image)
            cv.imshow('Gauss Image', self.gauss_image)
            cv.imshow('GradX Image', self.gradx_image)
            cv.imshow('GradY Image', self.grady_image)
            cv.imshow('SWT Image', self.swt_image*100)
        cv.destroyAllWindows()

    def store_images(self):
        """
        Method to store the Images
        """

        cv.imwrite('canny.png', self.canny_image)
        cv.imwrite('gauss.png', self.gauss_image)
        cv.imwrite('gradx.png', self.gradx_image)
        cv.imwrite('grady.png', self.grady_image)

    def execute_swt(self):
        """
        Method to execute the SWT Algorithm
        """

        self.initialize_images()

        Sx = -1*self.gradx_image
        Sy = -1*self.grady_image
        Gm = np.sqrt(Sx*Sx + Sy*Sy)
        Gx = Sx/(Gm+0.0001)
        Gy = Sy/(Gm+0.0001)

        for x in xrange(self.image_shape[1]):
            for y in xrange(self.image_shape[0]):
                if self.canny_image[y, x] > 0:
                    sx = Sx[y, x]
                    sy = Sy[y, x]
                    gm = Gm[y, x]
                    gx = Gx[y, x]
                    gy = Gy[y, x]

                    ray = []
                    ray.append((x, y))
                    px, py, i = x, y, 0
                    while True:
                        i = i+1
                        cx = math.floor(x + gx*i)
                        cy = math.floor(y + gy*i)

                        if (cx != px) or (cy != py):
                            try:
                                if self.canny_image[cy, cx] > 0:
                                    ray.append((cx, cy))
                                    # theta = self.theta_image[y, x]
                                    # alpha = self.theta_image[cy, cx]

                                    if math.acos(gx*(-Gx[cy, cx]) + gy*(-Gy[cy, cx])) < np.pi/2.0:
                                        width = math.sqrt((cx-x)**2 + (cy-y)**2)

                                        for (rx, ry) in ray:
                                            self.swt_image[ry, rx] = min(width, self.swt_image[ry, rx])
                                        self.rays.append(ray)
                                    break
                                ray.append((cx, cy))
                            except IndexError:
                                break

                            px = cx
                            py = cy

        for r in self.rays:
            med = np.median([self.swt_image[y, x] for (x, y) in r])
            for (x, y) in r:
                self.swt_image[y, x] = min(self.swt_image[y, x], med)

        self.visualize_images()
